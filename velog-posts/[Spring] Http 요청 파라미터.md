<h1 id="요청-데이터-전달-방법">요청 데이터 전달 방법</h1>
<ul>
<li><p>GET - 쿼리파라미터</p>
<ul>
<li><strong>/url?username=hello&amp;age=24</strong></li>
<li>메시지 바디 없음</li>
</ul>
</li>
<li><p>POST - HTML Form</p>
<ul>
<li>content-type : <strong>application/x-www-form-urlencoded</strong></li>
<li>메시지 바디에 쿼리 파라미터 형식으로 전달 <strong>username=hello&amp;age=24</strong></li>
</ul>
</li>
<li><p>Http 메시지 바디에 데이터를 직접 담아서 요청</p>
<ul>
<li>Http api에서 주로 사용, 바디 데이터 형식은 Json, xml, text</li>
<li>주로 Json 사용</li>
<li>POST, PUT, PATCH 메서드에서 주로 사용</li>
</ul>
</li>
</ul>
<br />
<br />
<br />


<h1 id="requestparam">@RequestParam</h1>
<p>만약 쿼리파라미터를 이용해 <code>/request-param?username=hello&amp;age=24</code>와 같은 uri 요청을 한다고하자.</p>
<pre><code class="language-java">

@Slf4j
@Controller
public class RequestParamController {

   @ResponseBody
    @RequestMapping(&quot;/request-param-v2&quot;)
    public String requestParamV2(
        @RequestParam(&quot;username&quot;) String memberName,
        @RequestParam(&quot;age&quot;) int memberAge) {

        log.info(&quot;username={}, age={}&quot;, memberName, memberAge);

        return &quot;ok&quot;;
    }

    @ResponseBody
    @RequestMapping(&quot;/request-param-v3&quot;)
    public String requestParamV3(
        @RequestParam String username,
        @RequestParam int age) {

        log.info(&quot;username={}, age={}&quot;, username, age);

        return &quot;ok&quot;;
    }


}
</code></pre>
<ul>
<li><p>v2와 같은 경우에는 메서드의 파라미터 이름과 쿼리파라미터의 key값이 일치하지 않아 <code>@RequestParam(&quot;username&quot;) String memberName</code>과 같이 옵션을 주어 memberName 파라미터에는 username이라는 쿼리 파라미터의 value값을 매핑한다(값을 넣어준다)</p>
</li>
<li><p>v3와 같이 메서드의 파라미터 이름과 쿼리파라미터의 key값이 일치하는 경우 옵션을 주지 않아도 되며, 심지어<code>@RequestParam</code>을 생략할 수 있다. 그러나 이 방법은 협업시에 생략하자고 약속되지 않았으면 다른사람이 알아볼 수 있게 생략하지 않는 것이 좋다.(아 ~ 쿼리파라미터의 username값을 메서드의 username이라는 파라미터로 받아오는거구나 ~ 라고 알 수 있도록)</p>
</li>
</ul>
<br />
<br />
<br />

<pre><code class="language-java">    @ResponseBody
    @RequestMapping(&quot;/request-param-required&quot;)
    public String requestParamRequired(
            @RequestParam(required = true) String username,
            @RequestParam(required = false) Integer age) {

        log.info(&quot;username={}, age={}&quot;, username, age);
        return &quot;ok&quot;;
    }

    @ResponseBody
    @RequestMapping(&quot;/request-param-default&quot;)
    public String requestParamDefault(
            @RequestParam(required = true, defaultValue = &quot;guest&quot;) String username,
            @RequestParam(required = false, defaultValue = &quot;-1&quot;) int age) {

        log.info(&quot;username={}, age={}&quot;, username, age);
        return &quot;ok&quot;;
    }

    @ResponseBody
    @RequestMapping(&quot;/request-param-map&quot;)
    public String requestParamMap(@RequestParam Map&lt;String, Object&gt; paramMap) {

        log.info(&quot;username={}, age={}&quot;, paramMap.get(&quot;username&quot;), paramMap.get(&quot;age&quot;));
        return &quot;ok&quot;;
    }
</code></pre>
<ul>
<li>다음과 같이 required 옵션을 통해 해당 파라미터 값이 필수인지 아닌지 지정할 수 있다.</li>
<li>defaultValue 옵션을 통해 기본값을 지정할 수 있다.</li>
<li>Map으로 값을 받아올 수도 있다.</li>
<li><strong>url?username=hello&amp;username&amp;world</strong>과 같이 하나의 파라미터에 여러 개의 값이 들어온다면 MultiValueMap으로 값을 받을 수 있다 ( key = &quot;username&quot;, value = [&quot;hello&quot;, &quot;world&quot;])</li>
</ul>
<br />
<br />
<br />
<br />
<br />
<br />

<h1 id="modelattribute">@ModelAttribute</h1>
<br />

<p>요청 파라미터를 받아 필요한 객체를 만들고 파라미터 값을 객체에 넣어주어야할 때가 있다.
요청 파라미터를 받아 다음과 같은 객체에 값을 넣어준다고 생각해보자.</p>
<pre><code class="language-java">@Data
public class HelloData {
    private String username;
    private int age;

}
</code></pre>
<p>만약 우리가 직접 파라미터값을 객체에 바인딩시켜준다면(넣어준다면) 아래와 같이 코드를 짜야한다. </p>
<pre><code class="language-java">@RequestParam String username;
@RequestParam int age;

HelloData data = new HelloData();

data.setUsername(username);
data.setAge(age);</code></pre>
<p>그러나 우리가 Http 요청마다 다음과 같이 반복되는 코드를 작성하는건 매우 비효율적이다.
그래서 스프링에서는 이 과정을 자동화해주는 <code>@ModelAttribute</code>라는 애노테이션을 제공한다.</p>
<br />
<br />


<pre><code class="language-java"> @ResponseBody
 @RequestMapping(&quot;/model-attribute-v1&quot;)
 public String modelAttributeV1(@ModelAttribute HelloData helloData){
      log.info(&quot;username={}, age={}&quot;, helloData.getUsername(), helloData.getAge());

      return &quot;ok&quot;;
 }</code></pre>
<p>스프링 MVC는 <code>@ModelAttribute</code>가 있으면 다음을 실행한다</p>
<ul>
<li>HelloData 객체를 생성</li>
<li>요청 파라미터의 이름으로 HelloData 객체의 프로퍼티를 찾아 setter를 호출해 파라미터의 값을 바인딩(입력)한다 (ex : 파라미터의 이름이 username이면 객체의 setUsername() 메서드를 찾아 호출하면서 값을 바인딩한다) </li>
</ul>
<p>여기서 프로퍼티란 객체의 필드를 말한다</p>