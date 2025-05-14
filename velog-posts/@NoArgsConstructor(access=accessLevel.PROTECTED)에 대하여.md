<h2 id="noargsconstructoraccess--accesslevelprotected란">@NoArgsConstructor(access = AccessLevel.PROTECTED)란?</h2>
<br />

<pre><code class="language-java">@Entity
@Getter
@NoArgsConstructor(access = AccessLevel.PROTECTED)
public class Comment extends BaseEntity {

    ...

}
</code></pre>
<br />


<p>우리가 Spring Boot를 사용하여 프로젝트를 진행할 때, 보통 엔티티에 <code>@NoArgsConstructor(access = AccessLevel.PROTECTED)</code> 을 붙인다.</p>
<p>이게 대체 무엇이고 어떻게 동작하는 것일까?</p>
<p>자주 사용해야하는 애노테이션인만큼, 적용했을때 어떤 Effect가 나타나는지 잘 알아야 Side Effect에 대처할 수 있다.</p>
<p>그러나 사실 새로운 기술 스택을 배우다보면 한걸음 한걸음이 매우 더디고 기능 구현에 급급하기에 “이걸 왜 사용하지?” 라는 질문을 놓치거나, 하더라도 그 이유를 찾아보는 건 뒤로 미루기 쉽상이다.</p>
<p>나 역시 처음에 Spring Boot를 사용해 프로젝트를 진행할 때도 그랬다.</p>
<ol>
<li>엔티티에 따로 <code>@Builder</code>나 생성자를 따로 설정해주는데, <code>@NoArgsConstructor</code> 은 왜 필요한걸까?</li>
<li>왜 accessLevel은 PUBLIC, PRIVATE이 아니고 PROTECTED지?</li>
</ol>
<p>위와 같은 의문점이 들었음에도 질문에 대한 답을 뒤로 미루다 미루다 여기까지 와버린 것이다..</p>
<br />
<br />


<p>그렇다면 <code>@NoArgsConstructor(access = AccessLevel.PROTECTED)</code> 란 무엇일까?</p>
<p><code>@NoArgsConstructor</code> 는 기본생성자(파라미터가 없는 생성자)를 뜻하는 것이고, 해당 생성자의 access level을 protected로 설정한다는 것이다.</p>
<p>만약 Comment 엔티티의 클래스 레벨에 <code>@NoArgsConstructor(access = AccessLevel.PROTECTED)</code> 아래와 같은 생성자를 생성해준다.</p>
<pre><code class="language-java">protected Comment() {
}</code></pre>
<br />
<br />
<br />

<h2 id="noargsconstructor는-왜-사용할까">@NoArgsConstructor는 왜 사용할까?</h2>
<p><code>@NoArgsConstructor(access = AccessLevel.PROTECTED)</code> 가 무엇인지에 대해서 알아보았으니 이제 근본적인 질문으로 돌아가보자.</p>
<p>엔티티의 클래스 레벨에 <code>@NoArgsConstructor</code> 는 왜 사용할까?</p>
<br />
<br />


<h3 id="1-jpa의-객체-생성-방식">1. JPA의 객체 생성 방식</h3>
<p>JPA는 데이터베이스와의 상호작용을 위해 엔티티 객체를 생성할 때 리플렉션(reflection)을 사용하며, 리플렉션을 통해 클래스의 기본 생성자를 호출하여 객체를 생성한다. 
따라서 기본 생성자가 없으면 JPA는 해당 엔티티를 인스턴스화할 수 없다.</p>
<br />

<h3 id="2-프록시-객체-생성">2. 프록시 객체 생성</h3>
<p><img alt="" src="https://velog.velcdn.com/images/alsgudtkwjs/post/2d96d690-cf49-4e02-8692-b0f6c6fde3e5/image.png" /></p>
<p>JPA는 Lazy Loading(지연 로딩)과 같은 기능을 지원하기 위해 엔티티의 프록시 객체를 생성할 수 있다. 이 프록시 객체는 껍데기이며, target이라는 변수에 호출할 객체의 참조값을 가지고 있다.
그리고 실제 객체가 필요할 때까지 로딩을 지연시키는 역할을 한다. 
프록시 객체는 위에서 언급했듯이 껍데기이기 때문에 프록시 객체를 생성하려면 생성하기 위해서도 기본 생성자가 필요하다.</p>
<br />

<h3 id="3-직렬화-및-역직렬화">3. 직렬화 및 역직렬화</h3>
<p><img alt="" src="https://velog.velcdn.com/images/alsgudtkwjs/post/2279c89b-5fa1-46af-b0fa-a6d19cfb5ee7/image.png" /></p>
<p>직렬화된 데이터(예: JSON, XML 등)를 객체로 변환할 때, 역직렬화 라이브러리(예: Jackson, Gson 등)는 해당 클래스의 인스턴스를 생성해야 한다. 이때 기본 생성자를 사용하여 객체를 생성한다. 만약 기본 생성자가 없다면, 라이브러리는 객체를 생성할 수 없고, 결과적으로 역직렬화가 실패하게 된다.</p>
<br />
<br />
<br />
<br />

<h2 id="왜-noargsconstructor의-accesslevel이-protected일까">왜 @NoArgsConstructor의 AccessLevel이 PROTECTED일까?</h2>
<p>결론부터 말하자면 엔티의 <strong>Proxy 조회</strong> 때문이다.</p>
<p>정확히는 엔티티의 연관 관계가 맺어져있는 객체를 조회할 때 지연 로딩의 경우에는 실제 엔티티가 아닌 객체의 참조값을 가지는 프록시 객체를 조회한 후, 해당 객체의 데이터를 호출했을 때 프록시 객체가 해당 객체의 참조값을 통해서 조회한다.</p>
<p>프록시 객체를 사용하기 위해서 JPA 구현체는, 실제 엔티티의 기본 생성자를 통해 프록시 객체를 생성하는데, 이 때 접근 권한이 private이면 프록시 객체를 생성할 수 없는 것이다.</p>
<p>이 때 즉시로딩으로 구현하게 되면, 접근 권한과 상관없이 프록시 객체가 아닌 실제 엔티티를 생성하므로 문제가 생기지 않는다.</p>
<p>아래 예시를 통해 위 내용을 설명해보겠다.</p>
<br />
<br />

<pre><code class="language-java">@Getter
@NoArgsConstructor(access = AccessLevel.PROTECTED)
@Entity
public class User {
    @Id
    @Column(name = &quot;user_id&quot;)
    @GeneratedValue(strategy = GenerationType.IDENTITY)
    private Long id;

    private String password;

    @Builder
    public User(String password) {
        this.password = password;
    }
}
</code></pre>
<pre><code class="language-java">@Getter
@NoArgsConstructor(access = AccessLevel.PROTECTED)
@Entity
public class Posts {
    @Id
    @Column(name = &quot;post_id&quot;)
    @GeneratedValue(strategy = GenerationType.IDENTITY)
    private Long id;

    private String title;

    private String content;

    @ManyToOne(fetch = FetchType.LAZY)
    @JoinColumn(name = &quot;user_id&quot;)
    private User user;

    @Builder
    public Posts(String title, String content, User user) {
        this.title = title;
        this.content = content;
        this.user = user;
    }
}</code></pre>
<p>다음은 User와 Posts의 코드이다. User와 Posts는 1:N 관계로 맺어져있다.</p>
<br />
<br />

<pre><code class="language-java">@SpringBootTest
class ApplicationTests {

    @Autowired
    private EntityManager em;

    @BeforeEach
    void createData() {
        User user = User.builder()
                .password(&quot;goodjob!&quot;)
                .build();

        em.persist(user);

        Posts posts = Posts.builder()
                .title(&quot;글 제목입니다.&quot;)
                .content(&quot;글 내용입니다.&quot;)
                .user(user)
                .build();

        em.persist(posts);
    }

    @Test
    @Transactional
    void proxyTest() {
        Posts posts = em.find(Posts.class, 1L);

        System.out.println(&quot;postsId = &quot; + posts.getId());
        System.out.println(&quot;userId = &quot; + posts.getUser().getId());
    }
}</code></pre>
<p>Posts는 영속성 컨텍스트를 통해 조회하고, user는 프록시 객체를 통해서 조회하는 테스트이다.</p>
<p>다음의 케이스들에 따라(NoArgsConstructor의 접근권한을 다르게하여) 테스트 코드를 돌려보자.</p>
<ol>
<li>Posts, User모두 protected일 때</li>
<li>Posts는 protected, User는 private일 때</li>
<li>Posts는 private, User는 protected일 때</li>
</ol>
<br />
<br />

<h3 id="1-posts-user-모두-protected일-때">1. Posts, User 모두 protected일 때</h3>
<p><img alt="" src="https://velog.velcdn.com/images/alsgudtkwjs/post/032781a9-061b-4892-8dff-befb803cb6c2/image.png" /></p>
<p>이 경우에는 정상 출력 된다.</p>
<p>정상 출력 되는 이유는 <strong>접근 권한이 protected이므로, JPA 구현체가 User 프록시 객체를 정상적으로 생성하고</strong>, 실제 User 엔티티의 값이 필요해질 때 User 프록시 객체가 초기화를 통해서 실제 Entity를 참조해 값을 가져오기 때문이다.</p>
<br />

<h3 id="2-posts는-protected-user는-private일-때">2. Posts는 protected, User는 private일 때</h3>
<p><img alt="" src="https://velog.velcdn.com/images/alsgudtkwjs/post/32bd5cb8-2ce9-4cd6-9d1f-bb76362fbed4/image.png" /></p>
<p>이 경우에는 정상 출력되지 않고, 에러가 발생한다.
에러가 발생하는 이유는 <strong>User의 접근 권한이 private이기 때문에, 지연 로딩시 JPA 구현체가 User</strong> <strong>프록시 객체를 생성할 때 접근할 수 없기 때문이다.</strong></p>
<p>에러 로그를 보면 public, protected, package-private 접근자가 붙은 생성자를 찾을 수 없어 프록시를 호출할 수 없음을 알 수 있다.</p>
<pre><code>2024-08-11T16:27:41.448+09:00 ERROR 23708 --- [spring] [    Test worker] o.h.p.p.bytebuddy.ByteBuddyProxyFactory  : HHH000143: Bytecode enhancement failed because no public, protected or package-private default constructor was found for entity: umc.spring.domain.User. Private constructors don't work with runtime proxies

java.lang.NoSuchMethodException: umc.spring.domain.User$HibernateProxy$yAE50x9U.&lt;init&gt;()
    ...

org.hibernate.HibernateException: HHH000143: Bytecode enhancement failed because no public, protected or package-private default constructor was found for entity: example.spring.domain.User. Private constructors don't work with runtime proxies</code></pre><br />

<h3 id="3-posts는-private-user는-protected일-때">3. Posts는 private, User는 protected일 때</h3>
<p><img alt="" src="https://velog.velcdn.com/images/alsgudtkwjs/post/b29e9f5f-df84-4b93-b001-64fec71b26bd/image.png" /></p>
<p>이 경우에는 정상 출력 된다.</p>
<p>정상 출력 되는 이유는 Posts 엔티티는 접근 권한과 지연 로딩과는 상관 없이 em.find를 통해서 영속성 컨텍스트에서 실제 Entity 객체로 조회되기 때문이다. 그리고 User 엔티티는 접근 권한이 protected이기 때문에 정상적으로 Proxy 객체가 생성된다.</p>
<br />
<br />

<p>그러면 접근 권한이 PUBLIC일때도 프록시 객체를 생성할 수 있는게 아닌가?라는 의문이 들 수 있다.</p>
<p>우리가 객체를 생성하고 객체 안의 값을 채워넣는 방법에는 아래와 같이 2가지가 있다.</p>
<pre><code class="language-java">// 1. 기본생성자로 생성 후 setter로 필드 세팅
User user = new User();
user.setEmail(&quot;kim@gmail.com&quot;);
user.setName(&quot;Kim&quot;);

// 2. 매개변수를 가지는 생성자를 통해 객체를 생성함과 동시에 필드 세팅
User user = User.builder()
                .email(&quot;Kim@gmail.com&quot;)
                .name(&quot;Kim&quot;)
                .build();
</code></pre>
<p>1번 방법처럼 기본 생성자로 객체를 생성 후 setter를 통해 필드값을 주입하는 방법은 setter를 통해서 언제 어디서든 객체의 값을 변경할 수 있기에 나중에는 어디서 객체의 값을 변경했는지 추적하기 어렵고, 객체지향적으로도 옳지 못하기에 권장하는 방법이 아니다.</p>
<p>즉, 객체가 불변성을 만족하지 못한다.</p>
<p>JPA에서는 기본적으로 기본 생성자를 요구하는데, 이 때문에 <code>@NoArgsConstructor</code> 를 작성하게 된다. 그러나 위의 이유로 인해서 이러한 JPA의 Entity Class의 요구사항 이외에는 기본 생성자를 이용할 일이 없게 된다.
결국 2번을 통해서 무분별한 객체 생성을 방지하며, 접근 권한을 public이 아닌 protected로 제한함으로 최대한 접근 범위를 작게 가져가는 것이다.</p>
<br />
<br />

<h2 id="이슈">이슈</h2>
<pre><code class="language-java">    @BeforeEach
    void createData() {
        User user = User.builder()
                .password(&quot;goodjob!&quot;)
                .build();

        em.persist(user);

        Posts posts = Posts.builder()
                .title(&quot;글 제목&quot;)
                .content(&quot;글 내용&quot;)
                .user(user)
                .build();

        em.persist(posts);

        em.clear(); // 영속성 컨텍스트 비워주기
    }</code></pre>
<p>분명 User 엔티티를 <code>@NoArgsConstructor(access = AccessLevel.private)</code> 로 설정했는데, 자꾸 User의 id값이 정상적으로 불러와 졌다.. 그래서 이유가 뭔지 생각을 해보니 위의 코드에서 문제의 이유를 찾을 수 있었다.</p>
<p>문제가 생긴 이유는 바로 영속성 컨텍스트에 User와 Posts가 남아 있기 때문이다. 영속성 컨텍스트에 엔티티들이 남아있으면, JPA 구현체는 지연 로딩시 프록시 객체를 생성하지 않고, 영속성 컨텍스트에 남아있는 실제 엔티티를 이용하기 때문에 계속 Test가 성공했던 것이다.</p>
<p>따라서 데이터를 세팅해준 후 <code>em.clear()</code> 를 이용해서 영속성 컨텍스트를 비워줬더니 테스트가 기대했던대로 실패하였다!</p>
<h2 id="정리">정리</h2>
<p>내용을 정리하면 다음과 같다.</p>
<ul>
<li><code>@NoArgsConstructor(access = AccessLevel.PUBLIC)</code> : 기본 생성자를 이용하여, 값을 주입하는 방식을 최대한 방지하기 위해서 사용을 권장하지 않는다.</li>
<li><code>@NoArgsConstructor(access = AccessLevel.PROTECTED)</code> : 위, 아래와 같은 프록시 객체의 생성과 객체에 대한 접근 범위 문제를 해결하기 위해서 사용한다.</li>
<li><code>@NoArgsConstructor(access = AccessLevel.PRIVATE)</code> : 프록시 객체 생성시 문제가 생기기 때문에 사용을 권장하지 않는다.</li>
</ul>