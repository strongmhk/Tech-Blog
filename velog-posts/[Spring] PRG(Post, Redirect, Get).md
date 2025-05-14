<h1 id="문제상황">문제상황</h1>
<br />
<br />

<p><code>ItemController.java</code></p>
<pre><code class="language-java">    // class 레벨에 @RequestMapping(&quot;/basic/items&quot;)이 있다

    @GetMapping(&quot;/{itemId}&quot;)
    public String item(@PathVariable long itemId, Model model){
        Item item = itemRepository.findById(itemId);
        model.addAttribute(&quot;item&quot;, item);
        return &quot;basic/item&quot;;

    }

    @PostMapping(&quot;/add&quot;)
    // @ModelAttribute의 이름을 생략하면 클래스 이름의 맨앞만 소문자로 바꿔 모델에 저장
    // @ModelAttribute HelloItem item -&gt; model.addAttribute(&quot;helloItem&quot;, item);
    public String addItemV3(@ModelAttribute Item item){
        itemRepository.save(item);
        return &quot;basic/item&quot;;
    }


</code></pre>
<br />
<br />
<br />



<p><code>template/basic/item.html</code></p>
<pre><code class="language-html">&lt;!DOCTYPE HTML&gt;
&lt;html xmlns:th=&quot;http://www.thymeleaf.org&quot;&gt;
&lt;head&gt;
  &lt;meta charset=&quot;utf-8&quot;&gt;
  &lt;link th:href=&quot;@{/css/bootstrap.min.css}&quot;
          href=&quot;../css/bootstrap.min.css&quot; rel=&quot;stylesheet&quot;&gt;
  &lt;style&gt;
    .container {
      max-width: 560px;
    }
  &lt;/style&gt;
&lt;/head&gt;
&lt;body&gt;
&lt;div class=&quot;container&quot;&gt;
  &lt;div class=&quot;py-5 text-center&quot;&gt;
    &lt;h2&gt;상품 상세&lt;/h2&gt;
  &lt;/div&gt;

  &lt;div&gt;
    &lt;label for=&quot;itemId&quot;&gt;상품 ID&lt;/label&gt;
    &lt;input type=&quot;text&quot; id=&quot;itemId&quot; name=&quot;itemId&quot; class=&quot;form-control&quot;
           value=&quot;1&quot; th:value=&quot;${item.id}&quot; readonly&gt;
  &lt;/div&gt;
  &lt;div&gt;
    &lt;label for=&quot;itemName&quot;&gt;상품명&lt;/label&gt;
    &lt;input type=&quot;text&quot; id=&quot;itemName&quot; name=&quot;itemName&quot; class=&quot;form-control&quot;
           value=&quot;상품A&quot; th:value=&quot;${item.itemName}&quot; readonly&gt;
  &lt;/div&gt;
  &lt;div&gt;
    &lt;label for=&quot;price&quot;&gt;가격&lt;/label&gt;
    &lt;input type=&quot;text&quot; id=&quot;price&quot; name=&quot;price&quot; class=&quot;form-control&quot;
           value=&quot;10000&quot; th:value=&quot;${item.price}&quot; readonly&gt;
  &lt;/div&gt;
  &lt;div&gt;
    &lt;label for=&quot;quantity&quot;&gt;수량&lt;/label&gt;
    &lt;input type=&quot;text&quot; id=&quot;quantity&quot; name=&quot;quantity&quot; class=&quot;form-control&quot;
           value=&quot;10&quot; th:value=&quot;${item.quantity}&quot; readonly&gt;
  &lt;/div&gt;
  &lt;hr class=&quot;my-4&quot;&gt;
  &lt;div class=&quot;row&quot;&gt;
    &lt;div class=&quot;col&quot;&gt;
      &lt;button class=&quot;w-100 btn btn-primary btn-lg&quot;
              onclick=&quot;location.href='editForm.html'&quot;
              th:onclick=&quot;|location.href='@{/basic/items/{itemId}/edit(itemId=${item.id})}'|&quot;
              type=&quot;button&quot;&gt;상품 수정&lt;/button&gt;
    &lt;/div&gt;
    &lt;div class=&quot;col&quot;&gt;
      &lt;button class=&quot;w-100 btn btn-secondary btn-lg&quot;
              onclick=&quot;location.href='items.html'&quot;
              th:onclick=&quot;|location.href='@{/basic/items}'|&quot;
              type=&quot;button&quot;&gt;목록으로&lt;/button&gt;
    &lt;/div&gt;
  &lt;/div&gt;
&lt;/div&gt; &lt;!-- /container --&gt;
&lt;/body&gt;
&lt;/html&gt;</code></pre>
<p><img alt="" src="https://velog.velcdn.com/images/alsgudtkwjs/post/e53b7972-6dbd-4973-84ac-1bbaa18cdcc2/image.png" /></p>
<p>위의 컨트롤러와 뷰 템플릿(thymeleaf) 파일을 보면, 상품을 상품 등록 폼을 통해 등록을 하면 
<code>http://localhost:8080/basic/items/add</code>로 post 요청이 전송되고 ItemRepository에 상품이 등록된 후 템플릿 파일인 <code>basic/item</code>이 호출된다
그런데 여기에는 문제가 있다.</p>
<br />
<br />
<br />



<p><img alt="" src="https://velog.velcdn.com/images/alsgudtkwjs/post/5c6cf17e-70cd-4572-8509-2c37fc881cf2/image.png" /></p>
<ol>
<li>상품 등록 폼의 페이지를 get으로 요청하면 상품 등록 폼이 응답됨</li>
<li>상품 등록 폼에서 데이터를 입력하고 저장을 선택하면 POST /add + 상품 데이터가 서버로 전송, 그리고 템플릿 뷰 반환</li>
<li>반환된 뷰에서 새로고침을 누르면 POST /add + 상품 데이터가 서버로 다시 전송(마지막으로 전송한 데이터를 전송함)</li>
<li>새로고침시에 계속 상품이 생성됨</li>
</ol>
<br />
<br />
<br />
<br />
<br />
<br />



<p><img alt="" src="https://velog.velcdn.com/images/alsgudtkwjs/post/6664005e-7242-4c8d-851b-dbfe705e0188/image.png" /></p>
<p>위의 url를 보면 /add이고 새로고침을 누르면 위와 같은 작업을 반복할 수 있다는 표시창이 뜬다
그렇다면 근본적인 이유가 무엇일까? 그것은 바로 url를 응답한게 아니고 템플릿 내부의 뷰를 응답했기 때문이다
@Controller는 return에 적은 이름의 논리이름을 뷰 리졸버를 통해 물리 이름으로 바꾸어 프로젝트 파일 내부의 <strong>template</strong> 폴더에서 리소스를 찾아 응답한다
즉, 이건 http url이 아니다
실제로 위에서 상품 등록 시 /add로 POST 요청을 보냈는데 응답된 뷰의 url도 동일하다
그렇기 때문에 새로고침시 계속 똑같은 요청이 반복되는 것이다
그럼 해결방법은? <strong>redirect를 통해 http url을 응답해주면 된다!</strong></p>
<br />
<br />
<br />
<br />
<br />
<br />


<h1 id="prgredirectattributes-활용">PRG,RedirectAttributes 활용</h1>
<p><img alt="" src="https://velog.velcdn.com/images/alsgudtkwjs/post/29a6dba1-b14b-4095-b2fc-640db22fb7d5/image.png" /></p>
<p>위 그림을 보면 Post 요청을 보낸 후 redirect를 통해 상품 상세 페이지를 get요청하는 url로 redirect해준다</p>
<pre><code class="language-java">    @PostMapping(&quot;/add&quot;)
    public String addItemV6(Item item, RedirectAttributes redirectAttributes){
        Item savedItem = itemRepository.save(item);
        redirectAttributes.addAttribute(&quot;itemId&quot;, savedItem.getId());
        redirectAttributes.addAttribute(&quot;status&quot;, true);
        return &quot;redirect:/basic/items/{itemId}&quot;;
    }</code></pre>
<p>컨트롤러를 다음과 같이 수정해준다
return에서 GET /basic/items/{itemId}으로 redirect 해준다
그러면 이제 응답된 상품 상세 페이지의 url이 바뀔 것이다!
<code>return &quot;redirect:/basic/items/&quot; + item.getId();</code>와 같이 id를 객체에서 직접 꺼내 보내면 url 인코딩과정에서 문제가 될 수 있기 때문에
<code>redirectAttributes.addAttribute(&quot;itemId&quot;, savedItem.getId())</code>를 사용해 redirect 모델에 값을 담아 응답해준다</p>
<br />
<br />
<br />
<br />
<br />
<br />


<p><img alt="" src="https://velog.velcdn.com/images/alsgudtkwjs/post/560e7190-b074-4781-afd6-03c84e90b535/image.png" /></p>
<p>잘 바뀌었다!
<code>items/3/status=true</code>로 잘 바뀌었다</p>
<p>위의 url에 쿼리파라미터로 status=true가 보이는데,
모델에 담으면 뷰에서 사용할 수 있다</p>
<pre><code>&lt;h2 th:if=&quot;${param.status}&quot; th:text=&quot;'저장 완료'&quot;&gt;&lt;/h2&gt;</code></pre><p>다음과 같이 모델에 담아넘기면 param이라는 모델에 기본적으로 담긴다
프로퍼티 접근식으로 모델에 담아 넘긴 값을 조회해 활용할 수 있다!</p>