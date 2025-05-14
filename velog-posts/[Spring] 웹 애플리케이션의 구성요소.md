<h1 id="📌웹-서버">📌웹 서버</h1>
<ul>
<li>HTTP 기반으로 동작</li>
<li>정적 리소스(HTML, CSS, JS, 이미지, 영상) 제공, 기타 부가기능</li>
<li>ex) NGINX, APACHE</li>
</ul>
<br />
<br />
<br />

<h1 id="📌wasweb-application-server">📌WAS(Web Application Server)</h1>
<ul>
<li><p>HTTP 기반으로 동작</p>
</li>
<li><p>웹 서버 기능 포함(정적 리소스 제공 가능)</p>
</li>
<li><p>프로그램 코드를 실행해 <strong>애플리케이션 로직</strong> 수행</p>
<ul>
<li>동적 HTML, HTTP API(JSON)</li>
<li>서블릿, JSP, 스프링 MVC</li>
</ul>
</li>
<li><p>ex) Tomcat Jetty, Undertow</p>
</li>
</ul>
<p>웹 서버와 WAS의 차이 : 웹 서버는 정적 리소스를 반환, WAS 애플리케이션 로직을 다룸</p>
<br />
<br />
<br />



<h1 id="📌웹-시스템-구성">📌웹 시스템 구성</h1>
<p><img alt="" src="https://velog.velcdn.com/images/alsgudtkwjs/post/4130cd24-4f16-4f6b-a3ef-3a96225e6a16/image.png" /></p>
<ul>
<li>정적 리소스는 웹 서버가 처리, 애플리케이션 로직과 같은 동적인 처리는 WAS에게 위임</li>
<li>정적 리소스가 많아지면 웹 서버를, 애플리케이션 리소스가 많이 사용되면 WAS를 증설해 효율적인 리소스관리 가능</li>
<li>웹 서버는 정적 리소스만 제공하기 때문에 잘 죽지 않는 반면, WAS 서버는 잘 죽는다. 이때 WAS와 DB의 장애가 발생 시 웹 서버가 오류 화면을 제공할 수 있다.</li>
</ul>
<br />


<p>웹 시스템은 다음과 같이 웹 서버, WAS, DB를 하나로 묶어서 하는게 좋다.
WAS도 웹 서버(정적 리소스 처리)의 역할을 할 수 있지만 WAS가 정적 리소스와 애플리케이션 로직을 모두 수행하려면 쉽게 과부하가 올 수 있다.
애플리케이션 로직은 웹 서비스를 구성하는데 있어 중요하고 값비싼 자원이기 때문에 <strong>역할의 분리</strong>를 통해 정적 리소스는 웹 서버가, 애플리케이션 로직은 WAS가 처리하는게 좋다.</p>
<br />
<br />
<br />



<h1 id="📌서블릿">📌서블릿</h1>
<h2 id="🎈서블릿을-사용하는-was의-이점">🎈서블릿을 사용하는 WAS의 이점</h2>
<p><img alt="" src="https://velog.velcdn.com/images/alsgudtkwjs/post/307df2e8-cffa-4081-97dc-93d6e57d8494/image.png" /></p>
<p>우리가 웹 애플리케이션을 직접 구현하려면 위의 내용들을 전부 구현해야할 것이다.
예를 들어, http 요청 메시지를 parsing 해주는 로직을 짜고 메시지의 바디 내용을 직접 파싱해준다거나.. 이런 복잡한 일들을 매 요청과 응답마다 해주어야한다.
그러나 WAS를 사용하면 이런 책임들은 모두 WAS가 지원하는 서블릿 객체가 대신 해준다.</p>
<br />
<br />
<br />


<h2 id="🎈예제">🎈예제</h2>
<p><img alt="" src="https://velog.velcdn.com/images/alsgudtkwjs/post/d473f35e-f44b-429d-871d-2351ed9384a6/image.png" /></p>
<ul>
<li>/hello 라는 URL이 호출되면 서블릿 코드가 실행</li>
<li>HTTP 요청 정보를 편리하게 사용할 수 있는 HttpServletRequest</li>
<li>HTTP 응답 정보를 편리하게 사용할 수 있는 HttpServletResponse</li>
<li>개발자가 HTTP 스펙을 매우 편리하게 사용할 수 있음</li>
</ul>
<br />
<br />
<br />

<h2 id="🎈http-요청-응답-흐름">🎈HTTP 요청, 응답 흐름</h2>
<p><img alt="" src="https://velog.velcdn.com/images/alsgudtkwjs/post/1f617ac6-0d08-424d-9ca9-793a3b19c57f/image.png" /></p>
<p>HTTP 요청이 들어오면</p>
<ul>
<li>WAS는 Request, Response 객체를 새로 만들어서 서블릿 객체호출</li>
<li>개발자는 Request 객체에서 HTTP 요청 정보를 편리하게 꺼내서 사용</li>
<li>개발자는 Response 객체에 HTTP 응답 정보를 편리하게 입력</li>
<li>WAS는 Response 객체에 담겨있는 내용으로 HTTP 응답 정보 생성</li>
</ul>
<br />
<br />
<br />


<h2 id="🎈서블릿-컨테이너">🎈서블릿 컨테이너</h2>
<ul>
<li>톰캣처럼 서블릿을 지원하는 WAS를 서블릿 컨테이너라고 함</li>
<li>서블릿 컨테이너는 서블릿 객체를 생성, 초기화, 호출, 종료하는 생명주기 관리</li>
<li>서블릿 객체는 요청이 들어올 때마다 새로 생성하는게 아닌, 최초 로딩 시점에 생성해두고 재활용(싱글톤, 모든 고객 요청은 동일한 서블릿 객체 인스턴스에 접근)</li>
<li><strong>공유 변수 사용 주의</strong></li>
<li>서블릿 컨테이너 종료시 함께 종료</li>
<li>동시 요청을 위한 멀티 쓰레드 처리 지원</li>
</ul>
<br />
<br />
<br />


<h1 id="📌동시-요청---멀티-스레드">📌동시 요청 - 멀티 스레드</h1>
<p><img alt="" src="https://velog.velcdn.com/images/alsgudtkwjs/post/17aeaa7b-9540-4aeb-ad88-50205e1be92b/image.png" /></p>
<p>다음과 같이 요청이 들어오면 WAS는 서블릿 객체를 호출해야하는데, 이 서블릿 객체는
누가 호출할까? 바로 스레드라는 친구가 호출해준다.</p>
<blockquote>
<p><strong>스레드</strong></p>
</blockquote>
<ul>
<li>애플리케이션 코드를 하나하나 순차적으로 실행해줌</li>
<li>자바의 메인 메서드를 main이라는 스레드가 실행해줌</li>
<li>스레드가 없다면 자바 애플리케이션이 실행 불가능</li>
<li>스레드는 한 번에 하나의 코드 라인만 수행</li>
<li>동시 처리가 필요하면 스레드를 추가로 생성</li>
</ul>
<br />
<br />
<br />



<h2 id="🎈단일-요청---스레드-하나-사용">🎈단일 요청 - 스레드 하나 사용</h2>
<p><img alt="" src="https://velog.velcdn.com/images/alsgudtkwjs/post/7f4f22fb-da1d-44a3-8a80-29bed7de881d/image.png" /></p>
<p>위 그림과 같이 요청이 들어오면 WAS가 서블릿 객체를 연결해주기 위해 스레드가 생성되고 해당 스레드가 서블릿 객체에 할당돼 서블릿 객체의 인스턴스가 응답된다 </p>
<br />
<br />
<br />


<h2 id="🎈다중-요청---스레드-하나-사용">🎈다중 요청 - 스레드 하나 사용</h2>
<p><img alt="" src="https://velog.velcdn.com/images/alsgudtkwjs/post/b6dde427-3ebf-4d6d-9f09-7775db2a896e/image.png" /></p>
<p>스레드를 하나만 사용하는데 2개의 요청이 들어오면 새로 들어온 요청때문에 기존에 들어온 요청 처리까지 지연이 된다.</p>
<br />
<br />
<br />



<h2 id="🎈요청마다-스레드-생성">🎈요청마다 스레드 생성</h2>
<p><img alt="" src="https://velog.velcdn.com/images/alsgudtkwjs/post/9b149c5f-c986-4a4d-9497-9b70f159f33e/image.png" /></p>
<p>요청이 들어올 때마다 스레드를 생성하면</p>
<ul>
<li>동시 요청을 처리 가능</li>
<li>리소스가 허용할 때까지 처리 가능</li>
<li>하나의 스레드가 지연돼도, 나머지 스레드 정상 동작</li>
</ul>
<p>과 같은 이점이 있지만</p>
<ul>
<li>스레드의 생성 비용이 비싼점</li>
<li>스레드의 컨텍스트 스위칭 비용</li>
<li>스레드 생성에 제한이 없음(고객 요청이 너무 많이 오면 그대로 스레드를 계속 생성해 CPU와 메모리가 감당을 하지못함)</li>
</ul>
<br />
<br />
<br />



<h2 id="🎈스레드-풀">🎈스레드 풀</h2>
<p>요청마다 스레드를 생성하는 것의 단점을 보완하기 위해 스레드 풀이라는 개념이 나온다.</p>
<p><img alt="" src="https://velog.velcdn.com/images/alsgudtkwjs/post/a362e7d8-ff98-49c1-9149-aff643b2c4b9/image.png" /></p>
<p>최대 실행 가능한 스레드의 개수를 정해놓고 그 이상의 요청이 들어오면 거절하거나, 특정 숫자만큼만 대기시킬 수 있다.
만약 스레드가 남아있으면 스레드 풀에서 꺼내 쓰고, 다쓰면 스레드 풀에 다시 반납한다.</p>
<br />
<br />
<br />

<h3 id="✅특징">✅특징</h3>
<ul>
<li>필요한 스레드를 스레드 풀에 보관하고 관리(스레드 풀에서 꺼내쓰고, 반납)</li>
<li>스레드 풀에 생성 가능한 스레드의 최대치를 관리(톰캣은 최대 200개 기본설정, 변경가능)</li>
<li>요청이 최대치를 넘겨 스레드 풀에 스레드가 없으면? -&gt; 기다리는 요청은 거절하거나 특정 숫자만큼 대기하도록 설정해 유연하게 관리 가능</li>
</ul>
<br />
<br />
<br />



<h3 id="✅장점">✅장점</h3>
<ul>
<li>스레드가 미리 생성돼 있으므로, 스레드를 생성하고 종료하는 비용이 절약되고, 응답 시간이 빠름</li>
<li>생성 가능한 스레드의 최대치가 정해져있어 너무 많은 요청이 들어와도 기존 요청은 안전하게 처리할 수 있음</li>
</ul>
<br />
<br />
<br />


<h3 id="✅실무에서의-활용">✅실무에서의 활용</h3>
<ul>
<li><p>WAS의 주요 튜닝 포인트는 최대 스레드 수임</p>
</li>
<li><p>너무 낮게 설정시 동시 요청이 많으면, 서버 리소스는 여유롭지만 클라이언트는 금방 응답 지연이 된다</p>
</li>
<li><p>너무 높게 설정하면, 동시 요청이 많을시 CPU 메모리 리소스 임계점 초과로 서버가 다운이 된다</p>
</li>
<li><p>장애 발생시</p>
<ul>
<li>클라우드면 서버부터 늘리고, 이후에 튜닝</li>
<li>클라우드가 아니면 열심히 튜닝</li>
</ul>
</li>
</ul>
<br />
<br />
<br />


<h1 id="📌html-http-api">📌HTML, HTTP API</h1>
<br />
<br />


<h2 id="🎈정적-리소스">🎈정적 리소스</h2>
<p><img alt="" src="https://velog.velcdn.com/images/alsgudtkwjs/post/da9b2ed8-050b-461e-8afd-352a75b86f76/image.png" /></p>
<br />
<br />
<br />


<h2 id="🎈동적-html-페이지">🎈동적 HTML 페이지</h2>
<p><img alt="" src="https://velog.velcdn.com/images/alsgudtkwjs/post/c3a5fd71-ff8b-4324-9b2d-da3fa7a7e62f/image.png" /></p>
<br />
<br />
<br />


<h2 id="🎈http-api">🎈HTTP API</h2>
<p><img alt="" src="https://velog.velcdn.com/images/alsgudtkwjs/post/f7fb4a8a-2f1d-4441-8269-b617930dca9c/image.png" /></p>
<p><img alt="" src="https://velog.velcdn.com/images/alsgudtkwjs/post/79900a07-67fb-4172-add2-6891cc7ecd7d/image.png" /></p>
<ul>
<li>HTML이 아니라 데이터만 주고받음, UI화면 필요시 클라이언트가 별도 처리</li>
<li>주로 JSON 형식 사용</li>
<li>앱, 웹 클라이언트, 서버 to 서버(주문 서버 -&gt; 결제 서버)</li>
</ul>
<br />
<br />
<br />



<h1 id="📌렌더링ssr-csr">📌렌더링(SSR, CSR)</h1>
<br />
<br />
<br />

<h2 id="🎈ssr서버-사이드-렌더링">🎈SSR(서버 사이드 렌더링)</h2>
<p><img alt="" src="https://velog.velcdn.com/images/alsgudtkwjs/post/5e4f78c0-0f67-4df1-9783-7231f0114056/image.png" /></p>
<ul>
<li>HTML안에 들어갈 내용을 전부 서버측에서 가공하고 넣어 최종 결과를 웹 브라우저에 전달</li>
<li>주로 정적인 화면에서 사용</li>
<li>관련기술 : JSP, 타임리프 -&gt; 백엔드 개발자</li>
</ul>
<br />
<br />
<br />

<h2 id="🎈csr클라이언트-사이드-렌더링">🎈CSR(클라이언트 사이드 렌더링)</h2>
<p>   <img alt="" src="https://velog.velcdn.com/images/alsgudtkwjs/post/2d0d6618-119b-4498-9c87-0ea25c5640cd/image.png" /></p>
<br />

<ul>
<li>HTML 결과를 자바스크립트를 사용해 웹 브라우저에서 동적으로 생성해 적용</li>
<li>주로 동적인 화면에서 사용, 웹 환경을 마치 앱처럼 필요한 부분부분 변경가능</li>
<li>ex) 구글 지도(구글 지도에서 화면을 옆으로 이동해도 URL이 바뀌지않음), Gmail</li>
</ul>
<p>참고로 React, Vue.js와 같은 CSR + SSR을 동시에 지원하는 프레임워크도 있다</p>