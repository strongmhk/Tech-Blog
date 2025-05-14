<p>보통 우리가 실제 프로젝트 이외의 연습을 할 때는 다음과 같이 println 메소드를 사용해 콘솔창에 출력한다 </p>
<pre><code class="language-java">String name = &quot;Spring&quot;;

System.out.println(&quot;name = &quot; + name);</code></pre>
<p>그런데, 다음과 같이 println 메소드는 단점이 여러가지 있다.
로그의 기능들을 살펴보면 그 단점을 더 명확히 이해할 수 있다.</p>
<h1 id="slf4j">Slf4j</h1>
<p><img alt="" src="https://velog.velcdn.com/images/alsgudtkwjs/post/2c1dedcd-48b5-4ee6-8e27-bad0832106b3/image.png" /></p>
<p>Slf4j는 스프링부트의 로깅 라이브러리인 spring-boot-starter-logging
에 포함되는 라이브러리이다.</p>
<p>Slf4j는 인터페이스이고, 그 구현체로 Logback과 같은 로그 라이브러리를 선택한다.</p>
<br />
<br />
<br />



<pre><code class="language-java">import lombok.extern.slf4j.Slf4j;
import org.slf4j.Logger;
import org.slf4j.LoggerFactory;
import org.springframework.web.bind.annotation.RequestMapping;
import org.springframework.web.bind.annotation.RestController;


//@Slf4j
@RestController
public class LogTestController {

private final Logger log = LoggerFactory.getLogger(getClass());

@RequestMapping(&quot;/log-test&quot;)
public String logTest() {
    String name = &quot;Spring&quot;;
    log.trace(&quot;trace log={}&quot;, name);
    log.debug(&quot;debug log={}&quot;, name);
    log.info(&quot; info log={}&quot;, name);
    log.warn(&quot; warn log={}&quot;, name);
    log.error(&quot;error log={}&quot;, name);
    log.debug(&quot;String concat log=&quot; + name);

    return &quot;ok&quot;;
    }
}</code></pre>
<ul>
<li><code>private final Logger log = LoggerFactory.getLogger(getClass());</code> 를 이용해 Logger 객체를 이용해 log를 찍을 수 있다</li>
<li>또는 <code>@Slf4j</code> 애노테이션을 이용하면 위와 같이 final 필드로 직접 선언하지 않고도 알아서 Logger 객체가 생성된다</li>
</ul>
<br />
<br />
<br />


<h1 id="로그-레벨">로그 레벨</h1>
<p>로그 레벨은 </p>
<p><strong>LEVEL: TRACE &gt; DEBUG &gt; INFO &gt; WARN &gt; ERROR</strong>(갈수록 레벨이 낮아진다)</p>
<p>와 같은 순서인데, Trace 레벨에서 출력하면 그 아래 레벨들의 로그가 모두 출력되고
Debug 레벨에서 로그를 출력하면 Trace 레벨을 제외한 모든 로그가 출력된다.</p>
<p>그런데, 실무에서는 개발 서버와 운영서버를 분리하는 경우가 대부분이다.
서버의 역할에 따라 개발서버에서는 Debug 레벨까지 찍고, 운영서버에서는 Info 레벨까지만 찍고싶을 수도 있다.</p>
<pre><code class="language-properties">#전체 로그 레벨 설정(기본 info)
logging.level.root=info

#hello.springmvc 패키지와 그 하위 로그 레벨 설정
logging.level.hello.springmvc=debug
</code></pre>
<p><code>application.properties</code> 파일에 위와 같은 설정을 넣어주면, 경로에 따라 로그 레벨을 설정해줄 수 있다</p>
<h1 id="주의할-점">주의할 점</h1>
<pre><code class="language-java">log.debug(&quot;debug log={}&quot;, name); // 1 
log.debug(&quot;debug log={}&quot; + name); // 2</code></pre>
<p>다음 1번과 2번의 차이가 있다.
2번의 경우에는 + 를 통한 연산이 일어나 메모리에 저장이 된다.
그러나 만약 info 레벨까지만 로그를 출력한다면, debug레벨에서 실행된 연산값은 출력되지않고, 계속 메모리에 남아있을 것이다.
결국! <strong>메모리 낭비</strong>가 일어난다.
그래서 무조건!! 1번의 방식으로 로그를 출력해야한다.
안그러면 시니어 개발자분께 맴매를 맞을 것이다!</p>