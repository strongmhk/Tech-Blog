<h1 id="📌ip">📌IP</h1>
<blockquote>
<p>IP는 &quot;인터넷 프로토콜&quot;을 의미합니다. 인터넷을 포함하여 네트워크에서 데이터 패킷의 통신 및 라우팅을 관리하는 일련의 규칙 및 규칙입니다. IP는 인터넷과 최신 네트워크 통신의 기반이 되는 TCP/IP 프로토콜 제품군의 필수적인 부분입니다.
-chatGPT</p>
</blockquote>
<p>쉽게말하면 사람들은 방대한 인터넷의 세계에서 자신만의 고유한 주소를 가지고, 그 주소는 서로를 식별하는데 있어 중요하다.
그래서 이 인터넷 세계에서는 IP라는 규칙안에서 자신만의 주소를 가지고 데이터를 주고받는 것이라고 생각하면 될 것 같다. 
또한 데이터가 섞이지 않게 <strong>패킷</strong>이라는 상자에 담아 주고받는다.</p>
<br />
<br />
<br />

<h2 id="🎈ip-패킷-정보">🎈IP 패킷 정보</h2>
<p><img alt="" src="https://velog.velcdn.com/images/alsgudtkwjs/post/4e462043-adac-414d-8698-8fc11daae659/image.png" /></p>
<ul>
<li>Header : 출발지와 목적지의 IP주소, 패킷의 크기 등이 담겨있다</li>
<li>PayLoad(본문) : 전송 데이터가 담겨있다</li>
</ul>
<br />
<br />
<br />




<h2 id="🎈ip-프토토콜의-한계">🎈IP 프토토콜의 한계</h2>
<p><img alt="" src="https://velog.velcdn.com/images/alsgudtkwjs/post/4f0adbde-3a51-41ce-81a3-d48466bab25b/image.png" /></p>
<p>데이터를 주고받는 경로는 많은 노드들로 복잡하게 얽혀져있다
따라서 데이터를 소실하거나, 순서가 엉켜 도착할 수 있다</p>
<ul>
<li>비연결성 : 패킷을 받을 대상이 없거나 서비스 불능 상태여도 패킷을 전송한다</li>
<li>비신뢰성 : 중간에 패킷이 사라지거나 순서가 뒤엉켜 도착할 수 있다</li>
<li>프로그램 구분 : 같은 IP를 사용하는 서버에서 통신하는 애플리케이션이 2개 이상이면?(웹 브라우저로 웹서핑을 하면서 음악을 스트리밍 하는 경우) -&gt; 방은 1개이지만 2명이 방에 들어오려고 하는 상황이다</li>
</ul>
<p>이런 IP의 문제점을 보완하고자 TCP 통신이 등장한다</p>
<br />
<br />
<br />


<h1 id="📌인터넷-프로토콜-스택의-4계층">📌인터넷 프로토콜 스택의 4계층</h1>
<p><img alt="" src="https://velog.velcdn.com/images/alsgudtkwjs/post/223d0d01-b8e3-4f47-81b0-93dd7edddbca/image.png" /></p>
<ul>
<li><p>애플리케이션 계층 : 사용자와 제일 가까운 계층으로, 최종 사용자의 애플리케이션과 직접적으로 상호작용한다</p>
</li>
<li><p>전송 계층 : 두 장치 간의 신뢰성 있는 데이터 전송을 담당하고, 주로 TCP와 UDP가 사용된다</p>
</li>
<li><p>인터넷 계층 :  IP 프로토콜을 사용하여 데이터 패킷을 전송하고 라우팅하는 계층이다</p>
</li>
<li><p>네트워크 인터페이스 계층 :  데이터를 전기신호로 변환한 뒤, 물리적 주소인 MAC 주소를 사용해, 알맞은 기기로 데이터를 전달하는 계층이다</p>
</li>
</ul>
<br />
<br />
<br />


<p><img alt="" src="https://velog.velcdn.com/images/alsgudtkwjs/post/7f5af051-36de-466e-9267-86d598284abb/image.png" /></p>
<p>다음은 Hello, world!라는 데이터를 패킷에 담아 다른 서버에 전송하는 과정을 설명하는 그림이다 </p>
<br />
<br />
<br />

<h1 id="📌tcp">📌TCP</h1>
<blockquote>
</blockquote>
<p>TCP(Transmission Control Protocol)은 TCP/IP 프로토콜 스위트의 핵심 프로토콜 중 하나로, 인터넷 및 대부분의 현대 네트워크의 기능을 담당합니다. TCP는 신뢰성이 있고 연결 지향적이며 스트림 지향적인 전송 계층 프로토콜입니다. 이는 네트워크에 연결된 장치들 간에 데이터의 신뢰성이 보장되고 순서대로 전달될 수 있도록 합니다.</p>
<br />
<br />

<blockquote>
<p><strong>TCP의 특징</strong></p>
</blockquote>
<ul>
<li>신뢰성 : TCP는 확인 및 재전송 메커니즘을 사용하여 데이터의 신뢰성을 보장합니다. 발신자가 수신자에게 데이터를 보낼 때, 수신자로부터 확인(ACK)을 기다립니다. 일정한 시간 내에 ACK을 받지 못하면 데이터가 손실되거나 전달되지 않았다고 가정하고 데이터를 재전송합니다. 이러한 과정은 데이터가 성공적으로 수신되고 수신자에게 확인되기까지 반복됩니다.</li>
<li>연결 지향 : TCP는 데이터 전송이 시작되기 전에 두 장치 간에 연결을 설정합니다. 이를 TCP 연결 또는 TCP 세션이라고 합니다. 연결 설정은 SYN, SYN-ACK, ACK로 이루어지는 3-way handshake 과정을 통해 수행되며, 두 장치가 데이터를 교환할 준비가 되었는지를 확인합니다. 연결이 설정되면 데이터를 두 방향으로 전송할 수 있습니다.</li>
<li>순서 보장 : TCP는 발신자가 수신자로부터 데이터를 보낼 때, 보낸 순서대로 데이터가 수신자에게 도착하도록 보장합니다. 파일 전송이나 웹 페이지의 콘텐츠 전달과 같이 데이터 무결성과 엄격한 순서가 필요한 애플리케이션에 중요한 기능입니다.</li>
<li>흐름 제어 : TCP는 빠른 발신자가 느린 수신자를 압도하지 않도록 흐름 제어 메커니즘을 사용합니다. 수신자는 ACK 패킷에서 윈도우 크기 정보를 보내어 더 많은 데이터를 수용할 준비가 되었음을 신호합니다. 발신자는 수신자의 윈도우 크기에 따라 전송 속도를 조절하여 수신자가 자신의 속도로 데이터를 처리할 수 있도록 합니다.</li>
</ul>
<br />
<br />
<br />
<br />




<p><img alt="" src="https://velog.velcdn.com/images/alsgudtkwjs/post/c3cf2fee-5a43-48d6-bafe-11e7499e88bf/image.png" /></p>
<p>다음과 같이 TCP/IP 통신에서 IP의 헤더에는 출발지와 목적지의 IP, TCP 헤더에는 출발지와 목적지의 PORT가 담김을 알 수 있다.</p>
<p>위에서 얘기했듯이 각 바이트마다 번호가 매겨져 순서가 보장되고, 3-way handshake의 방법으로 연결이 돼있음을 알 수 있다.</p>
<p><img alt="" src="https://velog.velcdn.com/images/alsgudtkwjs/post/51009d11-04d2-4b65-9ccf-beb59e5cacde/image.png" /></p>
<ol>
<li>클라이언트가 Syn을 보냄</li>
<li>서버가 Syn + ACK로 응답</li>
<li>클라이언트가 ACK를 보내며 연결됨</li>
</ol>
<p>TCP의 3 way handshake의 과정은 이러하며 최근에는 3번의 과정에서 클라이언트가 데이터도 같이 보낸다고 한다</p>
<p><img alt="" src="https://velog.velcdn.com/images/alsgudtkwjs/post/61c9a005-42b2-4d81-863e-efdfb8a6321f/image.png" /></p>
<p><img alt="" src="https://velog.velcdn.com/images/alsgudtkwjs/post/3b87b4cb-9efb-41a1-93ad-d7fde68417f3/image.png" /></p>
<p>다음의 그림을 보면 클라이언트와 서버 모두 데이터를 잘 받았는지 응답할 의무를 지고있어 데이터 전달을 보증할 수 있으며 순서 또한 보장할 수 있다</p>
<br />
<br />
<br />
<br />
<br />



<h1 id="📌udp">📌UDP</h1>
<blockquote>
</blockquote>
<p>UDP (User Datagram Protocol)는 TCP/IP 프로토콜 스위트의 다른 전송 계층 프로토콜로, TCP와는 다른 특징을 가지고 있습니다. UDP는 비연결성, 비신뢰성, 그리고 데이터그램 기반의 프로토콜로서, 간단하고 빠른 데이터 전송을 지원합니다</p>
<br />
<br />

<blockquote>
<p><strong>UDP의 특징</strong></p>
</blockquote>
<ul>
<li>하얀 도화지에 비유(기능이 거의 없음)</li>
<li>비연결성 :  TCP와 달리 UDP는 연결을 설정하지 않고 데이터를 전송합니다. 따라서 데이터를 보내기 전에 미리 연결을 설정할 필요가 없습니다. 이로 인해 연결 설정 및 해제에 따른 오버헤드가 없어 빠른 데이터 전송이 가능합니다.</li>
<li>비신뢰성 : UDP는 데이터 전송의 신뢰성을 보장하지 않습니다. 데이터가 수신자에게 정확히 전달되는지 여부를 확인하지 않고, 데이터 손실이 발생할 수 있습니다. 또한, 데이터의 순서가 보장되지 않을 수 있으며, 중복된 패킷이 수신될 수도 있습니다.</li>
<li>속도 : UDP는 데이터를 빠르게 전송하는 것을 목표로 합니다. 신뢰성을 보장하지 않고 데이터를 단순히 전송하는 것으로 인해 TCP보다 더 빠른 전송 속도를 제공합니다. 따라서 신속한 데이터 전송이 필요한 응용 프로그램에서 주로 사용됩니다.</li>
</ul>
<p>IP와 거의 같으며, PORT와 체크섬이 추가된 정도이다.
애플리케이션 계층에서 추가 작업이 필요하며, TCP와 비교하면 신뢰성은 떨어지지만 속도가 빠르다는 장점이있다.
그래서 실시간 스트리밍, 통화 등에 이용된다.</p>
<br />
<br />
<br />
<br />

<h1 id="📌port">📌PORT</h1>
<p><img alt="" src="https://velog.velcdn.com/images/alsgudtkwjs/post/be03fd6e-156f-41a4-98c1-76522d3985aa/image.png" /></p>
<p>포트는 다음과 같이 하나의 IP에서 프로세스를 구분하기 위해 사용된다.</p>
<br />
<br />
<br />


<h1 id="📌dns">📌DNS</h1>
<p><img alt="" src="https://velog.velcdn.com/images/alsgudtkwjs/post/f60fd906-faa6-4124-bfab-a02667ac2b7e/image.png" /></p>
<ul>
<li>IP는 기억하기 어렵고, 위 그림과 같이 변경될 수 있다.</li>
<li>따라서 우리는 DNS(Domain Name System)을 사용한다.</li>
<li>DNS는 전화번호부와 같아 우리의 IP(전화번호)를 등록하고 그에 해당하는 Domain(이름)이 매핑된다</li>
</ul>
<br />
<br />
<br />


<p><img alt="" src="https://velog.velcdn.com/images/alsgudtkwjs/post/b96f0a75-7f31-4cb0-9e54-83bfc48dea80/image.png" /></p>
<p>다음과 같이 IP주소 200.200.200.2가 google.com에 매핑돼 우리가 google.com에 요청을 보내면 DNS 서버에 접근해 해당 도메인에 매핑되는 IP를 가져와 해당 IP로 다시 요청을 보내는 매커니즘이다.</p>
<br />
<br />
<br />