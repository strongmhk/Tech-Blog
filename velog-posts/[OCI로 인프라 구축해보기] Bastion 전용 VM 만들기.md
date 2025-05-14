<h2 id="사전-준비">사전 준비</h2>
<blockquote>
<p>OKE를 생성하면서 자동으로 생성된 VPC, Subnet, NAT GW, IGW, Routing Table들이 있다는 가정하에 진행하는 것이므로 별도로 설정한 것이 없다면 생성해주어야한다.</p>
</blockquote>





<h2 id="bastion-host란">Bastion Host란?</h2>
<p>Bastion Host는 컴퓨터 네트워크에서 외부와 내부를 연결해주는 안전한 서버이다. 쉽게 말해, 이 서버는 인터넷과 서비스 내부 망의 중요한 시스템 사이에 위치해, 외부에서 들어오는 접근을 관리하고 보호하는 역할을 한다.</p>
<p>그렇다면 Bastion Host는 어떤 상황에 필요할까?</p>
<p><img alt="" src="https://velog.velcdn.com/images/alsgudtkwjs/post/1a82b7dc-87c2-4860-a2d1-9beee35647fc/image.png" /></p>
<p>최근 진행한 프로젝트에서 만들고자 했던 서비스의 시스템 구조도이다.
웹 애플리케이션 서버(WAS)와 모니터링 서버(Grafana, Prometheus)는 외부 인터넷에서 직접 접근할 수 없도록 사설망 내부에 배치한다. 이러한 서버는 오직 서비스 개발자만 접근할 수 있어야 하며, 외부인에게 노출되어서는 안된다.</p>
<p>이를 위해 AWS의 <strong>VPC(Virtual Private Cloud)</strong>나 OCI의 <strong>VCN(Virtual Cloud Network)</strong>와 같은 서비스를 활용하여 별도의 네트워크를 구축한다. 이 네트워크는 외부 인터넷과 통신할 수 있는 Public Subnet과 통신할 수 없는 Private Subnet으로 구분된다.</p>
<p>그리고 여기서 외부 인터넷과 통신할 수 없는 망에 위에서 언급한 WAS나 모니터링 서버등을 배치한다.
Private Subnet의 자원에 접근하기 위해 Bastion Host를 활용한다. Private Subnet의 자원은 외부 인터넷에서 직접 접근할 수 없지만, 같은 VPC 내부의 서브넷에서는 접근이 가능하다. 따라서 VPC 내에 Bastion Host를 구축하여 외부 인터넷을 사용하는 개발자가 Private Subnet의 자원에 접근할 수 있도록 한다.</p>
<p>이러한 구조를 통해 보안을 유지하면서도 필요한 리소스에 대한 접근을 원활하게 할 수 있으며 Bastion을 사용하는 이유이기도하다.</p>
<p>참고로 OCI에서는 Bastion Service를 제공하고 있으나, 우리 서비스에서는 CI/CD를 위한 젠킨스 서버에서 지속적으로 Bastion 서버에 ssh 접속을 해야하기 때문에, 발급받은 세션이 종료되면 다시 세션을 생성해야한다는 불편함이 있는 Bastion Service를 이용하지 않고 Bastion 전용 인스턴스를 생성해주었다.</p>
<h2 id="bastion-host-생성">Bastion Host 생성</h2>
<h3 id="1-os-인스턴스-종류-설정">1. OS, 인스턴스 종류 설정</h3>
<p><img alt="" src="https://velog.velcdn.com/images/alsgudtkwjs/post/392785c3-3fae-4075-b428-76a8fac746c9/image.png" /></p>
<p>먼저 OS이미지와 Shape을 생성해준다.
OS 이미지는 범용적인 우분투 22.04 버전을 선택해주었고, Bastion VM의 경우에는 프로그램을 실행시키거나 데이터를 저장하는 역할은 아니기 때문에 1OCPU와 1GB 메모리를 제공하는 프리티어인 E2.1 Micro Shape을 선택해주었다.</p>





<h3 id="2-네트워크-설정">2. 네트워크 설정</h3>
<p><img alt="" src="https://velog.velcdn.com/images/alsgudtkwjs/post/b9c55ab0-c849-41b0-a261-25f862e7e07e/image.png" /></p>
<p>사전에 생성한 VPC와 Public Subnet을 설정해주고, Public IP 주소를 할당한다.</p>
<h3 id="3-ssh-키-설정">3. SSH 키 설정</h3>
<p><img alt="" src="https://velog.velcdn.com/images/alsgudtkwjs/post/5a52111f-a117-474e-9164-5716273a4a6b/image.png" /></p>
<p>Bastion으로 원격 접속을 할 때 필요한 SSH 키를 설정해준 후 생성한다.</p>
<h3 id="4-ssh-접속">4. SSH 접속</h3>
<p><img alt="" src="https://velog.velcdn.com/images/alsgudtkwjs/post/d76c2342-1ae1-4789-a61c-feb4e963797d/image.png" /></p>
<p>SSH 클라이언트를 이용해서 원격 접속해준다!</p>