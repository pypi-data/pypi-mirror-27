<%inherit file="../base.mako"/>

<%block name="page_title">Sign Up</%block>

<%block name="content">
    <form method="post" action="${request.make_path('/sign-up')}" class="center">
        ${request.csrf_tag}

        <p class="danger">
            WARNING: If you for some reason create an account on this site, please be sure to use
            a password that you don't use on any other site. I make no guarantees that this site
            is secure since it's a side project based on other side projects (and there's no real
            reason to sign up anyway).
        </p>

        <div class="column">
            <input type="text" name="username" placeholder="Username (optional)" autofocus>
            <input type="email" name="email" placeholder="Email Address" required>
            <input type="password" name="password" placeholder="Password" required>
        </div>

        <div class="buttons">
            <input type="submit" value="Sign Up">
        </div>
    </form>
</%block>
