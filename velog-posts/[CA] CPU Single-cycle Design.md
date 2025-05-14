<br />
<br />
<br />


<h1 id="cpu-성능에-영향을-주는-요인">CPU 성능에 영향을 주는 요인</h1>
<blockquote>
</blockquote>
<ul>
<li>Instruction Count -&gt; 명령어의 개수</li>
<li>CPI -&gt; 명령어 1개 당 clock cycle</li>
<li>Clock Cycle Time(CCT) -&gt; clock 1 cycle을 수행하는 시간</li>
</ul>
<p>여기서 명령어 개수는 <strong>사용하는 ISA와 컴파일러의 최적화 옵션</strong>에 의해 결정이 되고, CPI와 CCT는 <strong>CPU 하드웨어</strong>에 의해 결정이 된다.</p>
<br />
<br />
<br />
<br />
<br />
<br />




<h1 id="cpu-구성요소">CPU 구성요소</h1>
<p><img alt="" src="https://velog.velcdn.com/images/alsgudtkwjs/post/0bbf8de7-1dd1-4f74-bba4-783ab8271e20/image.png" /></p>
<p><strong>Datapath</strong> : <strong>데이터의 실질적인 처리와 연산을 담당</strong>하는 CPU 구성 요소로, 산술 및 논리 연산을 수행하고 레지스터, ALU, multiplexer, 및 bus를 포함한다</p>
<p><strong>Control path</strong> : <strong>명령어의 실행을 관리하고 조정</strong>하는 CPU의 부분으로, 명령어 해독, 데이터 경로 제어, 및 제어 신호 생성을 담당한다</p>
<br />
<br />
<br />
<br />
<br />
<br />


<h1 id="명령어-실행">명령어 실행</h1>
<p>명령어를 실행하는 과정은 다음과 같다</p>
<ol>
<li>PC값을 읽어와 명령어를 fetch한다</li>
<li>레지스터 파일(레지스터 집합체)에 존재하는 레지스터 번호를 통해 레지스터 값을 읽는다</li>
<li>ALU를 이용해 산술, 논리 연산을 하거나 메인 메모리에서 데이터를 읽어오는 등의 로직을 수행한다</li>
<li>PC값을 갱신한다(PC = target address 혹은 PC = PC + 4)</li>
</ol>
<br />
<br />
<br />
<br />
<br />
<br />

<h1 id="datapath-구성요소">Datapath 구성요소</h1>
<br />
<br />

<h2 id="combinational-element">Combinational element</h2>
<p><img alt="" src="https://velog.velcdn.com/images/alsgudtkwjs/post/079b2472-7f91-4c9f-8c36-d5b4b4d389b4/image.png" /></p>
<p>입력값에 따라 결과값이 바뀌는, 데이터를 연산하는 circuit들을 의미한다
이전의 상태값을 저장할 수가 없다는 한계가 있어 state(sequential) element이 존재한다</p>
<br />
<br />
<br />
<br />


<h2 id="statesequential-element">state(sequential) element</h2>
<p>레지스터나 메모리에 컴퓨터의 현재 상태나 정보를 저장하기 위한 것이다
state element에는 어떤 것들이 있는지 알아보자</p>
<br />
<br />
<br />



<h3 id="s-r-latch">S-R latch</h3>
<p><img alt="" src="https://velog.velcdn.com/images/alsgudtkwjs/post/28253758-1eb8-4590-a66f-106307c39fb5/image.png" /></p>
<p>set-reset 자물쇠의 약자로 과거의 상태를 이용해서 다음 상태를 어떻게 유지할 것인지를 결정하는 서킷이다.
서킷을 보면 R과 S 앞에 있는 NOR 게이트의 input에 Q와 !Q가 들어가는 것을 볼 수 있다. 이는 <strong>이전의 Q값에 대한 정보</strong>이다.
Q와 !Q는 서로 같은 값을 가질 수 없으며 같은 값을 가지게 되는 경우에는 input이 거부된다.</p>
<br />
<br />
<br />

<p><img alt="" src="https://velog.velcdn.com/images/alsgudtkwjs/post/8632105d-1ffe-4be5-9a5a-3a38f4c6cb8e/image.png" /></p>
<br />

<p><img alt="" src="https://velog.velcdn.com/images/alsgudtkwjs/post/3bbba16b-f795-406d-81ce-50fe0b0f9d8f/image.png" /></p>
<br />

<ul>
<li><p>S와 R이 둘 다 0인 경우는 set과 reset을 모두 실행하지 않아 output 신호를 이전의 신호와 똑같이 유지한다</p>
</li>
<li><p>S와 R이 둘 다 1인 경우는 set과 reset을 모두 할 수 없으므로 회로의 구조상 정의에 위반되므로 invalid case로 판단하여 사용하지 않는다</p>
</li>
<li><p>S가 1, R이 0인 경우는 reset을 하지말고 set을 하라는 의미이므로 output이 1 이다.</p>
</li>
<li><p>S가 0, R이 1인 경우는 set을 하지말고, reset을 하라는 의미이므로 output은 0이 된다</p>
</li>
</ul>
<br />
<br />
<br />


<h3 id="d-latch">D latch</h3>
<p><img alt="" src="https://velog.velcdn.com/images/alsgudtkwjs/post/5cc772ac-0fc8-49ca-89b7-a9b1e48dbb4a/image.png" /></p>
<p>여기서 C는 Clock, D는 data의 약자이다
S와 R에 각각 1이 들어가지 않도록 해 invalid case를 처리한 circuit이다
C신호는 D 신호를 뒤로 넘길지 말지 결정한다</p>
<br />
<br />
<br />


<p><img alt="" src="https://velog.velcdn.com/images/alsgudtkwjs/post/bfc87e46-1127-4208-bf86-a7dd4d8ef3ab/image.png" /></p>
<p>C신호가 0이면 S와 R에 둘 다 0값이 인가되어 이전의 신호(state)가 유지된다(latch, 이전의 신호를 자물쇠로 걸어 잠군다)
C신호가 1이면 Q값을 D값으로 변경한다
즉,  C신호는 data를 뒤로 넘길지 말지를 결정한다</p>
<br />
<br />
<br />



<h3 id="flip-flop">flip-flop</h3>
<p><img alt="" src="https://velog.velcdn.com/images/alsgudtkwjs/post/8b35701d-f324-4c9a-ac45-1416cd211ae1/image.png" /></p>
<p>flip-flop은 D latch를 2개 이어서 만든 회로이며, 데이터를 저장을 한 후 data값을 갱신해서 다음의 값에 저장할 수 있는 로직을 구현하는 회로이다</p>
<br />
<br />
<br />



<p><img alt="" src="https://velog.velcdn.com/images/alsgudtkwjs/post/b5ff6a85-98da-4dd9-bc50-b22bbe7172bd/image.png" /></p>
<p> flip-flop의 특징은 C의 신호가 rising 하거나 falling 할 때 D의 값을 Q의 값으로 가져간다는 특징이 있다.</p>
<p>위 경우에는 C의 신호가 2번째 D latch로 가는 길에 NOT 게이트가 달려있기 때문에 Falling edge에서 D의 신호가 Q의 신호로 인가된다. 
Rising edge에 똑같은 기능을 구현하고 싶다면 NOT게이트를 1번째 D-latch로 가는 길에 달아주면 된다.</p>
<br />
<br />
<br />


<p><img alt="" src="https://velog.velcdn.com/images/alsgudtkwjs/post/ce301acf-a41b-452d-b4e1-8b0d700a6a85/image.png" /></p>
<p>위와 같이 clock의 주기(rising, falling edge)마다 D의 값이 Q로 유지되며 그 과정에서 약간의 delay가 발생한다.
이와 같이 flip-flop은 <strong>주기적으로 clock의 값에 따라 저장된 값을 update해야될 때 사용한다</strong></p>
<br />
<br />
<br />
<br />
<br />
<br />

<h3 id="clock-주기-설정-방법">Clock 주기 설정 방법</h3>
<p><img alt="" src="https://velog.velcdn.com/images/alsgudtkwjs/post/78de13ef-e19a-4750-9487-96342179ffb6/image.png" /></p>
<p>clock의 주기를 몇으로 설정해야하는가?</p>
<p>일반적으로 clock의 주기와 실행속도는 반비례한다.
예를 들어 clock의 speed가 1GHz와 4GHz라면, 주기는 4GHz인게 더 짧을 것이다.
그래서 우리는 일반적으로 주기를 짧게 해 실행속도를 빠르게 하면 좋겠다고 생각할 것이다.</p>
<p>하지만 그것에는 제약이 있다.
위의 그림을 보면 앞에 있는 flip flop의 출력이 뒤에 있는 flip flop의 입력으로 전달되는 시간에 delay가 존재한다 </p>
<p>따라서 combinational logic의 delay보다 clock cycle의 주기를 더 길게해야 combinational logic의 연산값이 전달될 수 있으므로 delay 시간의 최댓값이 하드웨어 설계 시 사용할 수 있는 clock 주기의 최소값을 결정한다</p>
<p>중간에 있는 combinational logic의 복잡도가 높아질수록 clock의 주기를 길게할 수 밖에 없다</p>
<p>요약하자면 <strong>최대로 delay되는 시간에 따라 clock의 주기를 결정할 수 밖에 없다</strong></p>
<br />
<br />
<br />
<br />
<br />
<br />



<h2 id="레지스터-파일">레지스터 파일</h2>
<p><img alt="" src="https://velog.velcdn.com/images/alsgudtkwjs/post/342d2fe6-f70d-437e-9d36-9f065e7846d0/image.png" /></p>
<p>flip-flop은 1비트 단위의
현재 상태의 값을 저장을 하고, 다음 상태의 값을 갱신해 저장하는 동작을 한다.
그래서 flip-flop을 데이터를 저장하는 용도인 레지스터로 사용한다</p>
<p>flip-flop은 1비트 단위로 저장하므로 1비트에 flip flop이 1개라고 볼 수 있다
각 register당 64비트로 이루어져 있으므로,  64개의 flip-flop이 있다</p>
<p>이 레지스터 파일에는 32개의 64비트 레지스터가 존재한다</p>
<br />
<br />
<br />
<br />
<br />
<br />



<h2 id="decoder">decoder</h2>
<p><img alt="" src="https://velog.velcdn.com/images/alsgudtkwjs/post/eb5f2d98-b002-4af3-be52-2630381b0670/image.png" /></p>
<p>decoder는 n비트의 input을 받아서 2^n개의 output을 만들어내고 one-hot 코딩을 통해 output값을 선택하는 동작을 한다.</p>
<p>decoder는 연산값의 결과를 어느 레지스터에 저장할지 선택해주는 역할을 한다</p>
<br />
<br />
<br />
<br />
<br />
<br />





<h1 id="레지스터-read-write">레지스터 Read, Write</h1>
<h2 id="read">Read</h2>
<p><img alt="" src="https://velog.velcdn.com/images/alsgudtkwjs/post/0faed5dd-bf66-49d2-9708-60e2f1d7352c/image.png" /></p>
<p>레지스터 값을 읽어오는 것은 <strong>32by1의 multiplexer(mux)</strong>를 이용해서 구현할 수 있다.
입력 값으로 레지스터의 번호가 주어지고 해당 레지스터에 저장된 값이 출력된다</p>
<br />
<br />
<br />


<h2 id="write">Write</h2>
<p><img alt="" src="https://velog.velcdn.com/images/alsgudtkwjs/post/b0ba61a1-c1d1-4407-b298-dbf3534f9382/image.png" /></p>
<p>다음과 같이 <strong>decoder</strong>를 사용해 <strong>one-hot</strong>형태로 선택된 레지스터에만 C의 신호를 1로 인가하고 나머지 레지스터에는 C 신호를 0으로 인가한 후 AND 연산을 통해 선택된 레지스터에만 연산의 결과값을 저장하도록 한다</p>
<p>이 예제에서는 0번 레지스터의 C신호가 1로 인가가 된다</p>
<br />
<br />
<br />
<br />
<br />
<br />


<h1 id="datapath">Datapath</h1>
<br />
<br />
<br />

<h2 id="instruction-fetch">Instruction Fetch</h2>
<p><img alt="" src="https://velog.velcdn.com/images/alsgudtkwjs/post/deeb06b3-33f0-4ef3-bd7a-f6fbfbc662ce/image.png" /></p>
<p><strong>Instruction memory</strong>라는 주어진 주소값에 있는 명령어를 읽어와서 signal을 내보내는 하드웨어가 있다. 그래서 명령어를 fetch하는 과정은 다음과 같다.</p>
<ol>
<li>현재 PC값을 input으로 받아서 수행해야하는 명령어의 주소를 찾는다.</li>
<li>내부적으로 명령어를 해석한다.</li>
<li>명령어를 내보낸 후 명령어 수행을 한다.</li>
<li>PC에다가 4를 더한다.(다음 명령어의 주소를 취한다.) 단위가 byte이고 명령어의 크기는 4bytes이므로 4를 더하는 것이다</li>
</ol>
<br />
<br />
<br />
<br />


<h3 id="fetch-component">Fetch Component</h3>
<br />
<br />

<p>Iinstruction Fetch시 다음의 연산이 필요하다</p>
<ul>
<li>PC로부터 메모리 주소를 받아와 해당 메모리에 접근해 instruction을 읽는다</li>
</ul>
<br />


<p><img alt="" src="https://velog.velcdn.com/images/alsgudtkwjs/post/f327661e-7af5-4937-b1ae-43b277469b8b/image.png" /></p>
<p>instruction fetch시 필요한 컴포넌트들은 다음과 같다</p>
<ul>
<li><p>PC register</p>
</li>
<li><p>Instruction Memory/Cache(우리가 일반적으로 생각하는 Memory는 CPU 외부에 존재하는 DRAM이지만, <strong>instruction memory</strong>는 <strong>CPU 내부에 존재하는 cache를 의미한다</strong>)</p>
</li>
<li><p>Adder to increment PC value</p>
</li>
</ul>
<br />
<br />
<br />
<br />
<br />
<br />


<h2 id="r-type-instruction">R-Type Instruction</h2>
<p><img alt="" src="https://velog.velcdn.com/images/alsgudtkwjs/post/879bdbd0-4455-43b9-8c04-36831f149907/image.png" /></p>
<p><img alt="" src="https://velog.velcdn.com/images/alsgudtkwjs/post/5348b880-70fb-4331-ae58-12f736357766/image.png" /></p>
<p>R타입의 명령어의 포맷과 R타입의 명령어를 구현하기 위한 회로는 다음과 같다.</p>
<br />
<br />

<p><strong>register file input</strong></p>
<ul>
<li><p>5비트의 레지스터 번호(0~31)</p>
</li>
<li><p>연산 결과 값 write data</p>
</li>
<li><p>RegWrite(때로는 연산 결과 값을 저장하지 않는 연산도 있기에 RegWrite 신호가 0이면 write 연산을 하지않고, RegWrite이라는 신호가 1이 되면 write register에 write data값을 저장한다)</p>
</li>
</ul>
<br />
<br />


<p><strong>ALU Operation</strong></p>
<p><img alt="" src="https://velog.velcdn.com/images/alsgudtkwjs/post/cae75127-d430-4fd4-b6c6-65e7c7ade6ea/image.png" /></p>
<p>register file에서 읽은 2개의 피연산자 값을 ALU로 보내주고 ALU가 연산을 한다
ALU는 ALU operation이라는 4비트의 신호를 받는데, 이는 명령어의 종류를 뜻한다</p>
<br />
<br />
<br />
<br />
<br />
<br />




<h2 id="d-typeloadstore-instruction">D-Type(Load/Store) Instruction</h2>
<br />
<br />
<br />

<p><img alt="" src="https://velog.velcdn.com/images/alsgudtkwjs/post/8f2c15e6-e06c-413e-abbc-1962de747f02/image.png" /></p>
<p>D타입 명령어를 구현하기 위해 다음과 같은 컴포넌트들이 필요하다</p>
<ul>
<li><p>Data memory : Load/Store 명령어의 경우 <strong>메모리 I/O 작업</strong>이 필요하기 때문에 메모리 컴포넌트가 필요하다</p>
</li>
<li><p>Sign-extend : 위의 예제와 같이 <code>LDUR X1, [X2, offset]</code> 명령어의 경우 <strong>base address(X2 register 값) + offset</strong> 연산을 해주어야한다. 
그런데 레지스터의 값은 64bit이나 offset 값은 9bit인 address 필드에서 가져온다. 그래서 instruction에서 읽어온 9비트의 offset값을 64비트로 확장해주는 역할을 한다.
여기서 메모리 주소는 상대 주소로 나타내므로 부호가 필요하다. 따라서 sign 비트를 사용한다.</p>
</li>
</ul>
<br />
<br />
<br />



<p><img alt="" src="https://velog.velcdn.com/images/alsgudtkwjs/post/3e7b61af-b317-4b3d-9d22-0b04e8f39546/image.png" /></p>
<p>D타입의 명령어의 포맷과 D타입의 명령어를 구현하기 위한 회로는 다음과 같다.
<strong>register file</strong>은 <strong>레지스터 집합체</strong>, <strong>data memory</strong>는 <strong>메모리</strong>라고 생각하면된다
<code>LDUR X1, [X2, offset]</code> 를 실행할 때 회로의 흐름을 살펴보자</p>
<br />

<ol>
<li><p>레지스터 파일 input으로 <strong>Read register1</strong>에 2라는 레지스터 번호가, <strong>Write Register</strong>에는 1이라는 레지스터 번호가 들어온다
또한 <strong>RegWrite</strong>에 1이라는 신호가 인가된다</p>
</li>
<li><p>X2 레지스터를 읽고, 읽은 <strong>base address</strong>를 <strong>1번째 ALU input</strong>으로 전달한다
address 필드에서 가져온 <strong>offset</strong>값이 Sign extend 컴포넌트를 거쳐 64비트로 확장된 후 <strong>ALU의 2번째 input</strong>으로 전달된다</p>
</li>
<li><p>ALU에서 <strong>base address + offset</strong> 연산을 통해 실제 메모리 주소값을 얻어낸 후 data memory로 전달한다</p>
</li>
<li><p>data memory에서 <strong>MemRead</strong>라는 신호가 1로 인가되어 받은 주소값으로 접근해 데이터를 읽고 레지스터 파일의 마지막 input인 Write data로 보내준다.
그 후 Write register 번호에 해당하는 레지스터(X1)에 write 작업을 실행한다</p>
</li>
</ol>
<br />


<p>Store 명령어의 경우 레지스터 파일의 <strong>Read register2</strong>값으로 <strong>메인 메모리에 저장할 data</strong>가 들어온다</p>
<br />
<br />
<br />


<h2 id="r--d-type-instruction">R &amp; D type instruction</h2>
<p><img alt="" src="https://velog.velcdn.com/images/alsgudtkwjs/post/28bc08b1-9f56-4e16-9d72-18716fd7899c/image.png" /></p>
<p>ALU의 2번째 input으로 전달되는 신호에 mux를 추가해 하나의 회로로 R과 D타입의 명령어를 지원할 수 있다.
ALUSrc 신호의 경우 피연산자의 레지스터값을 받을지 정하는 신호이다.
ALUSrc가 0이면 R타입의 명령어이므로 피연산자를 받고
1이면 D타입의 명령어이므로 나머지 1개의 피연산자가 존재하지 않아 받지 않고, offset을 64비트로 확장한 값을 받는다</p>
<br />
<br />
<br />
<br />
<br />
<br />



<h2 id="branch-instruction">Branch Instruction</h2>
<pre><code>CBZ X1,offset(=label)


SUBS XZR, X1, X2 
B.EQ offset</code></pre><p>Branch 명령어에는 다음의 2가지 포맷이 존재한다.
CBZ 명령어의 경우에는 읽은 레지스터값을 0과 비교해 0이면 PC + offset(19bit) 값으로 Branch하는 명령어이다</p>
<br />
<br />
<br />





<p><img alt="" src="https://velog.velcdn.com/images/alsgudtkwjs/post/a9143cbc-8de0-48ac-98e1-0ab4ad1a4639/image.png" /></p>
<p>branch 명령어를 수행하기 위한 datapath 구조는 이렇다
offset값을 64비트로 확장하는 sign extend 컴포넌트가 존재한다
Shiftleft2라는 컴포넌트는 word(4byte) 단위인 <strong>Offset값을 word -&gt; byte로 단위 변환</strong>을 해주기 위해 4를 곱해주는 역할을 한다
또한 덧셈기와 Zero인지 판단하는 ALU가 존재한다</p>
<br />
<br />
<br />



<h3 id="cbz-instruction">CBZ instruction</h3>
<p><img alt="" src="https://velog.velcdn.com/images/alsgudtkwjs/post/65f6c63f-07d8-4795-a2df-8ce0b4314be7/image.png" /></p>
<p><code>CBZ X1,offset(=label)</code> 명령어 수행 시 사실 그림과 달리 X1은 위의 a포트가 아닌 아래의 b포트로 이동한다.
그 후 Zero ALU에 <strong>ALU Operation</strong>이라는 신호가 0111로 인가된다.
ALU는 <strong>pass input b</strong> 연산을 통해서 b포트로 들어온 값을 result값으로 뱉어낸다.
Zero ALU는 Zero라는 신호를 result값이 0이면 1, 0이 아니면 0로 인가한다
Zero가 1이면 PC + offset, 0이면 PC + 4 연산을 수행한다</p>
<br />
<br />
<br />


<h3 id="subs-instruction">SUBS instruction</h3>
<p><img alt="" src="https://velog.velcdn.com/images/alsgudtkwjs/post/8e528202-1146-44fc-97af-0391fe4b79cd/image.png" /></p>
<p>SUBS 명령어를 수행 시 Zero ALU에는 두 개의 레지스터 값이 모두 들어오게 되고 ALU Operation 신호가 0110으로 인가되어 뺄셈 연산을 수행해 result값이 0인지 아닌지 체크한 후 PC값을 계산한다</p>
<br />
<br />
<br />
<br />
<br />
<br />





<h2 id="single-cycle-full-datapath">Single-Cycle Full Datapath</h2>
<p><img alt="" src="https://velog.velcdn.com/images/alsgudtkwjs/post/c34defa0-09a9-4ad6-85e6-10762d3536bb/image.png" /></p>
<p>PCSrc는 다음 명령어를 실행할지 아니면 분기할 지 결정하는 신호이다
ALU에서 만들어낸 Zero값을 PCSrc라는 신호로 보낸다
PCSrc 신호를 받는 mux는 1이면 PC + offset값을, 0이면 PC + 4 값을 선택한다</p>
<p>Single-Cycle의 전체 Datapath는 이렇다</p>
<br />
<br />
<br />
<br />
<br />
<br />

<h1 id="control-unit">Control Unit</h1>
<p><img alt="" src="https://velog.velcdn.com/images/alsgudtkwjs/post/cab47226-7cd7-42c0-a125-ba65678cdf50/image.png" /></p>
<p>datapath에서 mux나, ALU, 레지스터 파일, data memory등 컴포넌트에 다양한 신호들이 인가되었다.
다양한 신호들이 존재하는만큼 그 신호를 제어할 유닛이 필요한데, 그 유닛이 <strong>control unit</strong>이다.
control unit은 datapath를 관리하기 위해 컨트롤 신호들을 생성해서 제어하는 요소이다.
control unit에는 상위 계층에서 <strong>전체 신호 전달을 담당</strong>하는 <strong>Main Controller(Control)</strong>와 <strong>ALU Operation을 결정</strong>하는 <strong>ALU Control</strong>이 있다.
이렇게 두 계층으로 나눈 이유는 속도라던지 하드웨어 복잡도를 낮추기 위해서이다.</p>
<br />
<br />
<br />
<br />
<br />
<br />


<h2 id="alu-control">ALU Control</h2>
<p><img alt="" src="https://velog.velcdn.com/images/alsgudtkwjs/post/24a13f9e-8390-41bb-8ce7-74cf71e65c3e/image.png" /></p>
<p>ALU 연산은</p>
<ul>
<li>Load/Store - D type instruction</li>
<li>R type instruction</li>
<li>Compare Branch에서 Zero인지 확인하는 연산 (pass input, substract)</li>
</ul>
<p>에서 사용이 된다
그렇기에 우리는 ALU에 인가되는 신호를 세분화해서 제어할 필요가 있고 그것을 담당하는 것이 ALU Control이다
ALU Control이 ALU Operation을 정하는 2단계는 다음과 같다.</p>
<p><img alt="" src="https://velog.velcdn.com/images/alsgudtkwjs/post/15a31b2d-ccc4-4037-9c3a-22ee7b1e92e4/image.png" /></p>
<ol>
<li><p>이 Main Controller(Control)가 2비트의 <strong>ALUOp</strong> 값을 생성해 ALU Control으로 보내준다.
이 단계는 ALUOp값을 통해 미리 해당 명령어의 대분류를 정하는 단계이다.</p>
</li>
<li><p>ALU Control이  2비트의 ALUOp값과  명령어의 11비트 <strong>opcode</strong>를 받아 4비트의 ALU Operation을 결정한다.</p>
</li>
</ol>
<p>D타입, CBZ의 경우 ALUOp값이 정해져있지만, R타입의 경우 연산이 여러가지 이므로 ALUOp값으로는 구분이 불가능하다. 따라서 ALU Control이 필요한 것이다.</p>
<br />
<br />
<br />
<br />
<br />
<br />



<h2 id="main-controllercontrol">Main Controller(Control)</h2>
<p><img alt="" src="https://velog.velcdn.com/images/alsgudtkwjs/post/e15ef063-d6c8-413c-863b-80a820e62be3/image.png" /></p>
<p>다음은 Control이 생성하는 signal을 정리한 표이다.
X로 돼있는 부분은 <strong>Don't Care</strong>비트이다.
CBZ의 경우 opcode로 총 8비트를 할당하지만 <strong>6비트만 사용</strong>을 하고 
나머지 2자리는 0으로 채운다.</p>
<p>Reg2Loc: <strong>2번째 레지스터 파일에 들어갈 값</strong>을 정하는 신호이다</p>
<p>ALUSrc : Register files 뒤에 위치한 mux에게 전달되며, <strong>register files에서 읽은 데이터</strong>와 <strong>immediate</strong> 중에서 어떤 값을 ALU에게 전달할 것인지를 결정한다.</p>
<p>MemtoReg : <strong>Data memory unit에서 읽은 데이터</strong>와 <strong>ALU에서 계산된 데이터</strong> 중에서 어떤 데이터를 register에 전달해서 write을 할 건지를 결정한다.</p>
<p>RegWrite: <strong>레지스터에 데이터를 저장할 건지 아닌지</strong>를 결정한다.</p>
<p>MemWrite, MemRead: <strong>메모리에서 데이터를 읽을건지 쓸건지</strong>에 대한 정보를 Data memory unit에 전달한다.</p>
<p>Branch: 분기가 되면은 PC값에 label 데이터를 전달하기 위해 사용된다.</p>
<p>ALUOp0, 1: ALU control에게 어떤 Type의 명령어가 들어왔는지 알려주는 signal이다.</p>
<br />
<br />
<br />
<br />
<br />
<br />




<h1 id="single-cycle-processor의-한계">Single-Cycle Processor의 한계</h1>
<br />
<br />
<br />


<ul>
<li><p>가장 지연시간이 긴 부분(longest delay)가 전체 클럭 주기(clock period)를 결정한다.</p>
<ul>
<li>특히 치명적인 경로(경로가 길어서 delay가 클 확률이 높은): load instruction은 <strong>instruction memory → register → ALU → data memory → register</strong> (1 clock 사이클에 이 모든 동작이 수행돼야한다)</li>
</ul>
</li>
</ul>
<ul>
<li><p>다른 instruction에 다른 주기로 실행할 수 없다.</p>
<ul>
<li>모든 instruction은 한 clock cycle에 실행되어야 하며, 모두 같은 clock cycle time이어야 한다.</li>
</ul>
</li>
</ul>
<ul>
<li><p>설계 원칙(design principle)을 위배한다.</p>
<ul>
<li><p>making the common case fast(가장 일반적인, 자주 사용되는 경로를 빠르게 하라)를 위배.</p>
</li>
<li><p>가장 느린 것에 맞춰지니까.</p>
</li>
<li><p>자주 사용되는 경로를 빠르게 하려고 해봤자, 가장 느린 것에 맞춰짐. 50을 10으로 줄여봤자, 100이 존재하면 헛수고.</p>
</li>
</ul>
</li>
</ul>
<p>이런 이유들 때문에 실제로는 single cycle 구조를 사용하지는 않고, pipelining을 통해 성능을 향상시킬 수 있다</p>