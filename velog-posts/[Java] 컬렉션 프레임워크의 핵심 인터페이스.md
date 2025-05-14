<p><img alt="" src="https://velog.velcdn.com/images/alsgudtkwjs/post/f3f654cf-fca5-4b1a-9a1d-4011fa3dc046/image.png" /></p>
<blockquote>
<p>점선 화살표 : 의존한다
점선 삼각형 화살표 : 구현한다
실선 삼각형 화살표 : 상속받는다</p>
</blockquote>
<p>위 그림은 컬렉션 프레임워크의 클래스 다이어그램이다</p>
<br />
<br />



<h1 id="구조">구조</h1>
<p>참고로 인터페이스에 적혀있는 메소드는 모두 추상메소드이다</p>
<ul>
<li><p>collection : 쉽게 바구니라고 생각하면 된다. 물건을 담기 위한 바구니!</p>
<ul>
<li>add : 바구니에 물건을 집어넣을 때 사용하는 메소드</li>
<li>iterator : 바구니에 물건을 집어넣고, 바구니에 있는 물건을 꺼내려할 때 필요한 iterator를 반환한다 </li>
<li>size : 바구니에 담겨있는 물건의 개수를 반환한다</li>
</ul>
</li>
</ul>
<br />
<br />


<ul>
<li><p>iterator : 물건을 꺼내기 위한 인터페이스</p>
<ul>
<li>hasNext : 물건을 꺼낼 때, 막 꺼내는게 아니고 다음에 꺼낼 물건이 있는지 확인하고 꺼내야한다. 다음에 꺼낼 물건이 있는지 확인하는 메소드</li>
<li>next : 다음에 꺼낼 물건이 있으면 그 물건을 꺼내는 메소드</li>
</ul>
</li>
</ul>
<br />
<br />


<ul>
<li><p>List : 바구니에 있는 물건의 순서를 부여하는 자료구조(collection을 상속받음)</p>
<ul>
<li>ArrayList : List의 구현체(collection을 상속받는 List의 구현체이므로 collection의 추상메소드와 List의 추상메소드를 모두 구현한다)</li>
</ul>
</li>
</ul>
<br />
<br />


<ul>
<li><p>Set : 바구니에 있는 물건의 중복이 불가능한 자료구조(collection을 상속받음)</p>
<ul>
<li>HashSet : Set의 구현체(collection을 상속받는 Set의 구현체이므로 collection의 추상메소드와 Set의 추상메소드를 모두 구현한다)</li>
</ul>
</li>
</ul>
<br />
<br />



<ul>
<li><p>Map : 바구니에 있는 물건의 구분을 위해 유일한 key값을 value에 매핑시켜 담는 자료구조, Set에 의존한다(key값이 유일해야하기 때문에)</p>
<ul>
<li>HashMap : Map의 구현체<ul>
<li>get : key값을 매핑해 value를 가져옴<ul>
<li>ketSet : key값들을 모두 가져옴(key값은 중복 불가능이므로 Set타입으로 반환)</li>
<li>put : key값에 대한 value값을 매핑해 map에 담는다</li>
</ul>
</li>
</ul>
</li>
</ul>
</li>
</ul>