<h2 id="이슈">이슈</h2>
<pre><code class="language-bash">The dependencies of some of the beans in the application context form a cycle:

┌─────┐
|  securityConfig defined in file [/Users/gacgonswacademy06/Documents/dev/myaong/pplog/member-service/build/classes/java/main/myaong/popolog/memberservice/config/SecurityConfig.class]
↑     ↓
|  customOAuth2UserService defined in file [/Users/gacgonswacademy06/Documents/dev/myaong/pplog/member-service/build/classes/java/main/myaong/popolog/memberservice/oauth2/service/CustomOAuth2UserService.class]
↑     ↓
|  memberCommandServiceImpl defined in file [/Users/gacgonswacademy06/Documents/dev/myaong/pplog/member-service/build/classes/java/main/myaong/popolog/memberservice/service/MemberCommandServiceImpl.class]
└─────┘</code></pre>
<p>애플리케이션을 실행시켰더니 다음과 같이 Spring Security를 활용한 클래스들에서 의존성 순환 참조 오류가 일어나고 있었다.</p>





<h2 id="문제점">문제점</h2>
<pre><code class="language-java">@Configuration
@EnableWebSecurity
@RequiredArgsConstructor
public class SecurityConfig {

    private final CustomOAuth2UserService customOAuth2UserService;
    private final OAuth2SuccessHandler oAuth2SuccessHandler;
    private final JwtFilter jwtFilter;

    ...

    @Bean // 의존성 순환 참조
    public PasswordEncoder passwordEncoder() {
        return new BCryptPasswordEncoder();
    }
}</code></pre>
<pre><code class="language-java">@Service
@RequiredArgsConstructor
@Slf4j
public class CustomOAuth2UserService extends DefaultOAuth2UserService {
    private final MemberCommandService memberCommandService; // 의존성 순환 참조

    ...

}</code></pre>
<pre><code class="language-java">@Service
@RequiredArgsConstructor
@Transactional
public class MemberCommandServiceImpl implements MemberCommandService {
    private final PasswordEncoder passwordEncoder; // 의존성 순환 참조
        ...
}</code></pre>
<pre><code class="language-java">     // SecurityConfig            
    @Bean
    public PasswordEncoder passwordEncoder() {
        return new BCryptPasswordEncoder();
    }

    // CustomOAuth2UserService
    private final MemberCommandService memberCommandService;

    // MemberCommandServiceImpl
    private final PasswordEncoder passwordEncoder;</code></pre>
<p>현재 의존성 구조가 SecurityConfig → CustomOAuth2UserService → MemberCommandServiceImpl → PasswordEncoder(SecurityConfig에서 주입 받음) 이기 때문에 의존성 순환 참조 에러가 발생하는 것이었다.</p>
<p>일단 SecurityConfig가 CustomOAuth2UserService와 OAuth2SuccessHandler는 참조해야할 수 밖에 없기 때문에 해결 방법은</p>
<ol>
<li>CustomOAuth2UserService에서 MemberCommandServiceImpl을 주입받지 않도록 하기</li>
<li>MemberCommandServiceImpl에서 PasswordEncoder를 직접적으로 주입받지 않도록 하기</li>
</ol>
<p>2가지로 나뉘는 것 같다.</p>
<pre><code class="language-java">package myaong.popolog.memberservice.service;

import lombok.RequiredArgsConstructor;
import org.springframework.security.crypto.password.PasswordEncoder;
import org.springframework.stereotype.Service;

@Service
@RequiredArgsConstructor
public class PasswordService {

    private final PasswordEncoder passwordEncoder;

    public String encodePassword(String rawPassword) {
        return passwordEncoder.encode(rawPassword);
    }

    public boolean matches(String rawPassword, String encodedPassword) {
        return passwordEncoder.matches(rawPassword, encodedPassword);
    }
}
</code></pre>
<pre><code class="language-java">@Service
@RequiredArgsConstructor
@Transactional
public class MemberCommandServiceImpl implements MemberCommandService {
    private final PasswordService passwordService; // PasswordService 주입

    ...
}</code></pre>
<p>다음과 같이 PasswordService를 만들어 MemberCommandServiceImpl에서 주입받도록 시도해봤지만, </p>
<p>결국 SecurityConfig → CustomOAuth2UserService → MemberCommandServiceImpl → PasswordService → ** PasswordEncoder(SecurityConfig)**</p>
<p>로 계층만 하나 추가된 것이기 때문에 여전히 의존성 순환 참조 오류를 벗어날 수 없었다.</p>





<h2 id="해결">해결</h2>
<pre><code class="language-java">if (findMember == null) {
    // member 저장
    Member newMember = AuthConverter.toMember(oAuth2Response, RequiredInfo.PROFILE);
}</code></pre>
<p>현재 CustomOAuth2UserService에서 MemberCommandServiceImpl을 호출해서 소셜 로그인 시 최초 로그인한 사용자라면 DB에 Member 정보를 저장하는 로직을 호출하고 있다.</p>
<p>그렇다면 해결을 위해서는 결국 CustomOAuth2UserService가 참조하지 않는 클래스에서 PasswordEncoder를 주입받아 비밀번호 관련 비즈니스 로직을 처리해야 의존성 순환 참조 오류를 벗어날 수 있다고 생각했다.</p>
<pre><code class="language-java">@RestController
@RequiredArgsConstructor
@RequestMapping(&quot;/auth&quot;)
public class AuthController {

    private final AuthService authService;

        ...

}
</code></pre>
<pre><code class="language-java">@Service
@RequiredArgsConstructor
@Transactional
public class AuthServiceImpl implements AuthService {
    private final PasswordEncoder passwordEncoder;
    ...
}</code></pre>
<p>그래서 별도의 AuthServiceImpl 클래스를 만들어 해당 클래스에서 PasswordEncoder를 주입받아 비밀번호 관련 로직을 처리하도록 해서 해결할 수 있었다.결론적으로 SecurityConfig에서 주입하는 PasswordEncoder를 CustomOAuth2UserService가 참조하지 않는 클래스에서 주입받음으로써 해결했다.</p>
<p><img alt="" src="https://velog.velcdn.com/images/alsgudtkwjs/post/fa55aabf-8cad-4c66-b40e-6da061d1c5c9/image.png" /></p>





<h2 id="개선점">개선점</h2>
<p>이 문제를 해결했지만, 아직 잠재적인 문제가 남아있다는 생각이 들었다.</p>
<p>현재 CustomOAuth2UserService에서는 MemberCommandServiceImpl 뿐만 아니라 MemberQueryServiceImpl도 주입받고 있기 때문에 MemberQueryServiceImpl에서 인증과 관련된 비즈니스 로직을 호출하기 위해 AuthServiceImpl을 호출한다면 </p>
<pre><code class="language-text">SecurityConfig → CustomOAuth2UserService → MemberQueryServiceImpl 
→ AuthServiceImpl -&gt; PasswordEncoder(SecurityConfig)</code></pre>
<p>다음과 같은 의존성 순환 참조 오류가 일어날 수도 있다😅</p>
<h3 id="별도의-설정-정보-클래스-구성">별도의 설정 정보 클래스 구성</h3>
<pre><code class="language-java">
@Configuration
public class WebConfig implements WebMvcConfigurer {

    @Bean
    public PasswordEncoder passwordEncoder() {
        return new BCryptPasswordEncoder();
    }
}</code></pre>
<p>따라서 별도의 설정 클래스를 만들어 해당 설정 클래스에서 PasswordEncoder를 주입받으면 해결방안에 적었던 것처럼 추후 변경에 의해 의존성 순환참조가 재발되는 것에 대한 우려를 하지 않아도 된다.</p>