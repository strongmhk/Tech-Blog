<p>최근 개발했던 사내 업무 관리 플랫폼에서 <strong>엑셀 파일로 회원 일괄 등록</strong>하는 기능이 있었다.</p>
<p>이 기능은 아래 절차로 작동한다.</p>
<ol>
<li>엑셀 파일로 회원 정보를 업로드</li>
<li>데이터를 파싱해 <code>Member</code> 엔티티로 생성</li>
<li>생성된 데이터를 DB에 저장</li>
<li>저장된 회원의 이메일로 임시 비밀번호를 전송</li>
</ol>
<hr />
<h2 id="성능-병목의-원인">성능 병목의 원인</h2>
<p>당시 개발했던 로직은 아래처럼 데이터를 하나씩 저장하고 있었다.</p>
<pre><code class="language-java">for (MemberCreateRequestForExcel memberCreateRequestForExcel : memberCreateRequestForExcels) {
    Member createdMember = memberSaveService.save(
        MemberMapper.mapToMemberFromExcel(memberCreateRequestForExcel, encryptedPassword, profileImageUrl, agitUrl)
    );
}
</code></pre>
<p>이 방식은 아래처럼 작동된다.</p>
<h3 id="하나씩-insert">하나씩 INSERT</h3>
<pre><code class="language-sql">insert into member (name, nickname, ...)
values (name1, nickname1, ...);

insert into member (name, nickname, ...)
values (name2, nickname2, ...);

insert into member (name, nickname, ...)
values (name3, nickname3, ...);
</code></pre>
<p>회원 수가 많을수록 쿼리가 계속 발생하기 때문에 성능 병목이 발생하기 쉽다. 원했던 방식은 아래처럼 한 쿼리로 여러 데이터를 저장하는 것이었다.</p>
<h3 id="한-번의-bulk-insert">한 번의 Bulk INSERT</h3>
<pre><code class="language-sql">insert into member (name, nickname, ...)
values (name1, nickname1, ...),
       (name2, nickname2, ...),
       (name3, nickname3, ...);
</code></pre>
<hr />
<h2 id="왜-jpa--auto-increment로는-bulk-insert가-불가능할까">왜 JPA + Auto Increment로는 Bulk Insert가 불가능할까?</h2>
<p>원했던 쿼리는 이렇게 하나로 밀어 넣는 것이었지만,</p>
<p>JPA + Auto Increment로는 불가능하다. 이유는 아래와 같다.</p>
<h3 id="1-jpa는-pk-반환이-즉시-필요하다">1. JPA는 PK 반환이 즉시 필요하다</h3>
<ul>
<li>Auto Increment는 데이터를 저장하면서 <strong>DB가 PK를 생성</strong>한다.</li>
<li>JPA는 <code>EntityManager</code> 내에서 엔티티를 계속 추적해야 하기 때문에, INSERT 직후 생성된 PK를 즉시 반환받아 엔티티 속성을 채워줘야 한다.</li>
<li>이렇게 해야 다른 연관관계나 변경 감지가 가능해진다.</li>
</ul>
<h3 id="2-jpa는-원래-쓰기-지연write-behind을-통해-모았다가-한-번에-flush-가능">2. JPA는 원래 쓰기 지연(Write-Behind)을 통해 모았다가 한 번에 flush 가능</h3>
<ul>
<li>원칙적으로 JPA는 여러 변경 작업을 모아두었다가 <code>flush()</code> 시점에 한 번에 실행하는 것이 가능하다.</li>
<li>하지만 PK 생성 후 반환이 필요한 Auto Increment 상황에서는 즉시 INSERT를 해야 PK를 알 수 있으므로, 데이터를 모아둔 후 한 번에 INSERT하는 것이 불가능해진다.</li>
</ul>
<h3 id="3-결국-하나씩-insert될-수밖에-없다">3. 결국 하나씩 INSERT될 수밖에 없다</h3>
<ul>
<li>위 이유로 <code>Auto Increment</code>는 <code>values(...),(...),(...);</code> 같은 Bulk Insert 문으로 만들 수 없으며,</li>
<li>데이터를 저장하는 순간마다 즉시 <code>INSERT → PK 반환</code> 과정이 발생하게 된다.</li>
</ul>
<hr />
<h2 id="해결-방법-spring-data-jdbc의-batchupdate-활용하기">해결 방법: Spring Data JDBC의 batchUpdate 활용하기</h2>
<p>PK 생성 전략을 SEQUENCE 방식으로 바꾸면 JPA를 사용하는 상황에서도 bulk 연산이 가능하도록 만들 수 있다. </p>
<p>하지만 PK 생성 전략을 바꾸면 애플리케이션 단에서 PK를 관리해야한다는 부담도 있고 Auto Increment 전략을 고려하고 작성된 로직 또한 변경돼야한다는 부담이 있어 선택하지 않았다.</p>
<p>현재 상황에서 더 간단한 방법이 있다. JDBC의 <code>batchUpdate</code> 기능을 사용하는 것이다</p>
<p>Spring Boot는 <code>Spring Data JPA</code>를 사용할 때 자동으로 <code>Spring Boot Starter JDBC</code>도 함께 의존성을 추가해준다.</p>
<p>이 덕분에 원한다면 동일 애플리케이션 내에서 <strong>JDBC batch</strong> 기능도 사용할 수 있다.</p>
<p>JDBC batch를 통해서는 PK 반환이 필요하지 않은 경우 한 번의 쿼리로 여러 데이터를 저장하는 것이 가능하다.</p>
<hr />
<h2 id="성능-비교-실험">성능 비교 실험</h2>
<p>아래는 동일 조건(1000명의 회원 저장)에서 <code>save</code>, <code>saveAll</code>, 그리고 <code>batchUpdate</code>로 데이터를 저장했을 때의 성능 측정 코드이다.</p>
<h3 id="성능-측정-테스트-코드">성능 측정 테스트 코드</h3>
<pre><code class="language-java">// JPA save 단건 반복 저장
@Test
void saveMemberTest() {
    List&lt;MemberEntity&gt; members = createTestMembers(1000);
    long start = System.currentTimeMillis();
    for (MemberEntity member : members) {
        memberSaveService.saveMember(member);
    }
    long end = System.currentTimeMillis();

    System.out.println(&quot;JPA save 단건 반복 저장 시간: &quot; + (end - start) + &quot;ms&quot;);
    Assertions.assertThat(memberRepository.count()).isEqualTo(1000);
}

// JPA saveAll 저장
@Test
void saveAllMemberTest() {
    List&lt;MemberEntity&gt; members = createTestMembers(1000);
    long start = System.currentTimeMillis();
    memberSaveService.saveAllMember(members);
    long end = System.currentTimeMillis();

    System.out.println(&quot;JPA saveAll 저장 시간: &quot; + (end - start) + &quot;ms&quot;);
    Assertions.assertThat(memberRepository.count()).isEqualTo(1000);
}

// JDBC batchUpdate 저장
@Test
void bulkInsertMemberTest() {
    List&lt;MemberCreateRequestForExcel&gt; requests = createTestMembers(1000).stream()
        .map(member -&gt; MemberCreateRequestForExcel.builder()
            .name(member.getName())
            .department(member.getDepartment())
            .position(member.getPosition())
            .phone(member.getPhone())
            .role(member.getRole())
            .nickname(member.getNickname())
            .email(member.getEmail())
            .profileImage(member.getProfileImage())
            .agitUrl(member.getAgitUrl())
            .build())
        .collect(Collectors.toList());

    List&lt;String&gt; passwords = Collections.nCopies(1000, &quot;icO8V*2hQIIC&quot;);

    long start = System.currentTimeMillis();
    memberSaveService.bulkInsertMember(requests, passwords);
    long end = System.currentTimeMillis();

    System.out.println(&quot;JDBC bulkInsert 저장 시간: &quot; + (end - start) + &quot;ms&quot;);
    Assertions.assertThat(memberRepository.count()).isEqualTo(1000);
}
</code></pre>
<hr />
<h2 id="성능-측정-결과">성능 측정 결과</h2>
<h3 id="jpa-save-반복-사용">JPA save 반복 사용</h3>
<p><img alt="" src="https://velog.velcdn.com/images/alsgudtkwjs/post/e7a7bb27-1f7b-4332-9c6c-7db1d6e1b32d/image.png" /></p>
<h3 id="jpa-saveall-사용">JPA saveAll 사용</h3>
<p><img alt="" src="https://velog.velcdn.com/images/alsgudtkwjs/post/3beb5b98-a367-49f6-a356-865f578e62b1/image.png" /></p>
<h3 id="jdbc-batchupdate-사용">JDBC batchUpdate 사용</h3>
<p><img alt="" src="https://velog.velcdn.com/images/alsgudtkwjs/post/ccf7d797-82e4-44af-99c8-a92428da9bac/image.png" /></p>
<table>
<thead>
<tr>
<th>저장 방식</th>
<th>시간</th>
</tr>
</thead>
<tbody><tr>
<td>JPA save 단건 반복</td>
<td>2,107 ms</td>
</tr>
<tr>
<td>JPA saveAll</td>
<td>1,845 ms</td>
</tr>
<tr>
<td>JDBC batchUpdate</td>
<td>170 ms</td>
</tr>
</tbody></table>
<p>결과적으로 JDBC batchUpdate를 통해 저장했을 때,</p>
<ul>
<li><code>save()</code> 대비 약 <strong>91.9%</strong> 성능 향상</li>
<li><code>saveAll()</code> 대비 약 <strong>90.8%</strong> 성능 향상이 가능했다.</li>
</ul>
<hr />
<h2 id="성능-차이가-발생하는-이유">성능 차이가 발생하는 이유</h2>
<h3 id="jpa-save">JPA save</h3>
<ul>
<li>데이터를 하나씩 저장하면서 매번 INSERT 쿼리를 생성한다.</li>
<li>PK를 반환해야하고, 변경 감지가 발생해 성능 저하가 일어난다.</li>
</ul>
<h3 id="jpa-saveall">JPA saveAll</h3>
<ul>
<li>여러 트랜잭션이 아닌 동일 트랜잭션 내에서 여러 데이터를 저장해 <code>save()</code>보다 효율적이다.</li>
<li>하지만 여전히 PK 반환과 변경 감지가 필요해 완전 Bulk 처리는 불가하다.</li>
</ul>
<h3 id="jdbc-batchupdate">JDBC batchUpdate</h3>
<ul>
<li>PK 반환과 변경 감지가 필요 없을 때 유용하다.</li>
<li>하나의 쿼리로 데이터를 밀어넣어 성능이 좋다.</li>
</ul>
<hr />
<h2 id="batchupdate를-사용할-때-고려해야-하는-점">batchUpdate를 사용할 때 고려해야 하는 점</h2>
<p><code>batchUpdate</code>는 성능 면에서 매우 강력하지만, 아래 점도 함께 고려해야 한다.</p>
<ul>
<li><strong>영속성 컨텍스트 활용 불가</strong>: <code>batchUpdate</code>로 저장된 데이터는 JPA 영속성 컨텍스트로 관리되지 않으며 변경 감지가 불가능하다.</li>
<li><strong>PK 반환 불가</strong>: Auto Increment로 생성된 PK를 즉시 반환받을 수 없다. 저장 후 생성된 ID를 활용하는 로직이 필요한 경우 적절하지 않다.</li>
<li><strong>엔티티 생명주기 무관</strong>: 저장된 데이터는 엔티티 생명주기(예: <code>persist</code>, <code>update</code> 등)나 연관관계 로직과 무관하게 작동된다.</li>
<li><strong>데이터베이스 의존도 증가</strong>: JPQL이 아닌 네이티브 SQL을 직접 작성(DB에 종속적)하기 때문에 변경 시 JPA보다 유지보수 부담이 높아질 수 있다.</li>
</ul>
<hr />
<h2 id="정리">정리</h2>
<p><code>batchUpdate</code>는 대용량 데이터를 저장하는데 매우 효율적인 방법이다.</p>
<p>단, PK 반환과 변경 감지가 필요 없고 비즈니스 로직과 연관되지 않은 데이터 저장 상황에서 활용하는 것이 권장된다.</p>
<p>그 외 상황에서는 JPA의 <code>save()</code>나 <code>saveAll()</code> 같은 표준적인 방법과 함께 고려해 성능과 유지보수 사이에서 적절한 Trade‑off를 판단하는 것이 중요하다.</p>