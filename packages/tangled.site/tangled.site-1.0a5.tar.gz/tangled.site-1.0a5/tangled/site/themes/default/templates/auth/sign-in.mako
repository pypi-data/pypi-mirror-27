<%inherit file="../base.mako"/>

<%block name="page_title">Sign In</%block>

<%block name="content">
    <form method="post" action="${request.make_path('/sign-in')}" class="center">
        ${request.csrf_tag}

        <div class="column">
            <input name="username" type="text" placeholder="Username or email address" required autofocus>
            <input name="password" type="password" placeholder="Password" required>
        </div>

        <div class="buttons">
            <input type="submit" value="Sign In">
        </div>

        ## If the came_from param is present, that indicates that the user
        ## was redirected here when attempting to access a protected page.
        ## Otherwise, the user clicked the "Sign In" link or accessed the
        ## /sign-in page directly.
        <% came_from = request.params.get('came_from') or request.referer or '' %>

        <input type="hidden" name="came_from" value="${came_from}">
    </form>
</%block>
