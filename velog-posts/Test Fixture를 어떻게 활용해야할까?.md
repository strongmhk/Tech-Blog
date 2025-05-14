<h2 id="test-fixture란"><strong>Test Fixture란?</strong></h2>
<p><strong>테스트 픽스처(Test Fixture)</strong>는 소프트웨어의 테스트를 수행하기 위해 필요한 데이터 또는 상태를 일관되게 설정하는 장치이다. 이는 특정 종류의 테스트에 필요한 환경을 만들고, 테스트의 독립성을 유지하는 데 중요한 역할을 한다. 안정적인 테스트 결과를 위해서는 테스트마다 고정된 상태를 확보하는 것이 중요하다.</p>


<h2 id="test-fixture-구성-방법">Test Fixture 구성 방법</h2>
<h3 id="1-테스트-케이스마다-fixture-만들기">1. 테스트 케이스마다 Fixture 만들기</h3>
<p>테스트 케이스가 서로 독립적이도록 구성하는 것은 중요하다. 각 테스트 메서드에서 필요한 Fixture를 생성하여 독립성을 보장할 수 있다. 
예를 들어, 댓글 작성 및 삭제에 대해 아래와 같이 성공 케이스 및 예외 케이스에 각각 독립적으로 테스트 데이터를 세팅해줄 수 있다.</p>
<pre><code class="language-java">public class TestExample {

    @Test
    public void createComment() {
        // Given
        Member member = new Member(1L, &quot;member1@example.com&quot;, &quot;password&quot;, &quot;name&quot;, &quot;nickname&quot;, &quot;department&quot;, &quot;position&quot;, &quot;phone&quot;, Role.USER, &quot;profileImage&quot;);
        Post post = new Post(1L, &quot;Test Title&quot;, &quot;Test Content&quot;);

        // When
        Comment comment = new Comment(member, post, &quot;This is a comment&quot;);

        // Then
        assertNotNull(comment);
        assertEquals(member, comment.getMember());
        assertEquals(post, comment.getPost());
        assertEquals(&quot;This is a comment&quot;, comment.getContent());
    }

    @Test
    public void deleteComment() {
        // Given
        Member member = new Member(1L, &quot;member1@example.com&quot;, &quot;password&quot;, &quot;name&quot;, &quot;nickname&quot;, &quot;department&quot;, &quot;position&quot;, &quot;phone&quot;, Role.USER, &quot;profileImage&quot;);
        Post post = new Post(1L, &quot;Test Title&quot;, &quot;Test Content&quot;);
        Comment comment = new Comment(member, post, &quot;This is a comment&quot;);

        // When
        comment.delete();

        // Then
        assertTrue(comment.isDeleted()); // Comment 클래스에 isDeleted() 메서드가 있다고 가정
    }

    @Test
    public void createCommentWithEmptyContent() {
        // Given
        Member member = new Member(1L, &quot;member1@example.com&quot;, &quot;password&quot;, &quot;name&quot;, &quot;nickname&quot;, &quot;department&quot;, &quot;position&quot;, &quot;phone&quot;, Role.USER, &quot;profileImage&quot;);
        Post post = new Post(1L, &quot;Test Title&quot;, &quot;Test Content&quot;);

        // When &amp; Then
        assertThrows(IllegalArgumentException.class, () -&gt; { // 예외 발생 검증
            new Comment(member, post, &quot;&quot;); // 빈 문자열은 허용하지 않는다고 가정
        });
    }

    @Test
    public void createCommentWithNullContent() {
        // Given
        Member member = new Member(1L, &quot;member1@example.com&quot;, &quot;password&quot;, &quot;name&quot;, &quot;nickname&quot;, &quot;department&quot;, &quot;position&quot;, &quot;phone&quot;, Role.USER, &quot;profileImage&quot;);
        Post post = new Post(1L, &quot;Test Title&quot;, &quot;Test Content&quot;);

        // When &amp; Then
        assertThrows(NullPointerException.class, () -&gt; { // 예외 발생 검증
            new Comment(member, post, null); // null은 허용하지 않는다고 가정
        });
    }
}
</code></pre>


<h3 id="2-하나의-클래스-내에서-test-fixture-통합하기">2. 하나의 클래스 내에서 Test Fixture 통합하기</h3>
<p>JUnit의 <code>@BeforeEach</code> 어노테이션을 사용하여 각 테스트 케이스에 필요한 Fixture를 한 번에 설정할 수도 있다. 이 방법은 가독성을 높일 수 있지만, 테스트 간의 결합을 유발할 수 있다.</p>
<pre><code class="language-java">public class TestExample {
    private Member member;
    private Post post;

    @BeforeEach
    public void setUp() {
        member = new Member(1L, &quot;member1@example.com&quot;, &quot;password&quot;, &quot;name&quot;, &quot;nickname&quot;, &quot;department&quot;, &quot;position&quot;, &quot;phone&quot;, Role.USER, &quot;profileImage&quot;);
        post = new Post(1L, &quot;Test Title&quot;, &quot;Test Content&quot;);
    }

    @Test
    public void testCommentCreation() {
        Comment comment = new Comment(member, post, &quot;This is a comment&quot;);

        assertNotNull(comment);
        assertEquals(member, comment.getMember());
        assertEquals(post, comment.getPost());
        assertEquals(&quot;This is a comment&quot;, comment.getContent());
    }

    @Test
    public void testModifyCommentContent() {
        Comment comment = new Comment(member, post, &quot;Original comment&quot;);

        comment.setContent(&quot;Modified comment&quot;);

        assertEquals(&quot;Modified comment&quot;, comment.getContent());
    }

    @Test
    public void testDeleteComment() {
        Comment comment = new Comment(member, post, &quot;This is a comment&quot;);

        comment.delete();

        assertTrue(comment.isDeleted()); // Comment 클래스에 isDeleted() 메서드가 있다고 가정
    }

    @Test
    public void testCreateCommentWithEmptyContent() {
        assertThrows(IllegalArgumentException.class, () -&gt; { // 예외 발생 검증
            new Comment(member, post, &quot;&quot;); // 빈 문자열은 허용하지 않는다고 가정
        });
    }

    @Test
    public void testCreateCommentWithNullContent() {
        assertThrows(NullPointerException.class, () -&gt; { // 예외 발생 검증
            new Comment(member, post, null); // null은 허용하지 않는다고 가정
        });
    }
}
</code></pre>


<h2 id="내가-선택한-방법">내가 선택한 방법</h2>
<p>필자는 <strong>테스트 케이스마다 Fixture를 만드는 것</strong>을 선호한다. 이렇게 하면 각 테스트 메서드가 필요한 상태를 명확하게 설정할 수 있고, 서로 영향을 주지 않으며 독립적으로 테스트를 수행할 수 있다.</p>
<p>Test Fixture를 사용할 때의 본질적인 목적은 <strong>일관된 환경을 만들고, 결과의 반복 가능성을 높이는 것</strong>이다. 일반적으로 Fixture를 구성할 때, 복잡한 테스트의 경우 각 테스트에 특화된 Fixture가 유용하다.</p>
<p>위의 예제에서와 같이, 다양한 <code>MemberFixture</code> 데이터를 아래와 같은 enum으로 만들어 적용할 수 있으며 이는 데이터 생성의 일관성과 재사용성을 높이는 데 도움을 준다.</p>
<pre><code class="language-java">@Getter
public enum MemberFixture {
    ADMIN_A(29L, &quot;admin1@gmail.com&quot;, &quot;AdminPass01*&quot;, &quot;관리자1&quot;, ...),
    ADMIN_B(30L, &quot;admin2@gmail.com&quot;, &quot;AdminPass02*&quot;, &quot;관리자2&quot;, ...),
        ...

        private final Long memberId;
    private final String email;
    ...

    MemberFixture(
        Long memberId,
        String email,
        ...
    ) {
        this.memberId = memberId;
        this.email = email;
        ...
    }

    public Member toMember() {
        return Member.builder()
            .memberId(memberId)
            .email(email)
            ...
            .build();

}
</code></pre>


<p>위와 같은 구조로 <code>MemberFixture</code>와 <code>PostFixture</code> 를 만들었을 때, 다양한 테스트 케이스에서 미리 정의된 데이터를 호출해서 간단하게 사용할 수 있다. </p>
<pre><code class="language-java">import org.junit.jupiter.api.Test;
import static org.junit.jupiter.api.Assertions.*;

public class TestExample {

    @Test
    public void testCommentCreation() {
        // Given
        Member member = MemberFixture.ADMIN_A.toMember();
        Post post = PostFixture.POST_A.toPost();

        // When
        Comment comment = new Comment(member, post, &quot;This is a comment&quot;);

        // Then
        assertNotNull(comment);
        assertEquals(member, comment.getMember());
        assertEquals(post, comment.getPost());
        assertEquals(&quot;This is a comment&quot;, comment.getContent());
    }

    @Test
    public void testModifyCommentContent() {
        // Given
        Member member = MemberFixture.ADMIN_A.toMember();
        Post post = PostFixture.POST_A.toPost();
        Comment comment = new Comment(member, post, &quot;Original comment&quot;);

        // When
        comment.setContent(&quot;Modified comment&quot;);

        // Then
        assertEquals(&quot;Modified comment&quot;, comment.getContent());
    }

    @Test
    public void testDeleteComment() {
        // Given
        Member member = MemberFixture.ADMIN_A.toMember();
        Post post = PostFixture.POST_A.toPost();
        Comment comment = new Comment(member, post, &quot;This is a comment&quot;);

        // When
        comment.delete();

        // Then
        assertTrue(comment.isDeleted()); // Comment 클래스에 isDeleted() 메서드가 있다고 가정
    }

    @Test
    public void testCreateCommentWithEmptyContent() {
        // Given
        Member member = MemberFixture.ADMIN_A.toMember();
        Post post = PostFixture.POST_A.toPost();

        // When &amp; Then
        assertThrows(IllegalArgumentException.class, () -&gt; { // 예외 발생 검증
            new Comment(member, post, &quot;&quot;); // 빈 문자열은 허용하지 않는다고 가정
        });
    }

    @Test
    public void testCreateCommentWithNullContent() {
        // Given
        Member member = MemberFixture.ADMIN_A.toMember();
        Post post = PostFixture.POST_A.toPost();

        // When &amp; Then
        assertThrows(NullPointerException.class, () -&gt; { // 예외 발생 검증
            new Comment(member, post, null); // null은 허용하지 않는다고 가정
        });
    }
}
</code></pre>