<!DOCTYPE html>

<%namespace file="auth/sign-out-form.mako" import="sign_out_form" />

<html lang="en">
    <head>
        <meta name="viewport" content="width=device-width, initial-scale=1.0">

        <link rel="shortcut icon" href="${request.make_url('favicon.ico')}"/>

        <title>${settings['site.title']}</title>

        <link rel="stylesheet" href="${request.static_path('/static/main.css')}"/>
    </head>

    <body>
        <ul id="meta-nav" class="nav nav-right">
            % if not user:
                <li><a href="${request.make_path('/sign-up')}">Sign Up</a></li>
                <li><a href="${request.make_path('/sign-in')}">Sign In</a></li>
            % else:
                <li><span>${request.user.name or request.user.username }</span></li>
                <li><a href="${request.resource_url('profile')}">Profile</a></li>

                % if user.has_role('admin'):
                    <li><a href="${request.resource_url('admin')}">Admin</a></li>
                % endif

                <li>${sign_out_form()}</li>
            % endif
        </ul>

        <header>
            <%block name="header">
                <a href="/">
                    <h1 class="title">${settings['site.title']}</h1>
                    <div class="tagline">${settings['site.tagline']}&nbsp;</div>
                </a>
            </%block>
        </header>

        <ul id="main-nav" class="nav">
            % if user and user.has_role('admin'):
                <li><a href="${request.resource_url('admin')}">Admin</a></li>
            % endif

            <li><a href="/">Home</a></li>

            <li>
                <a href="${settings['site.entries.path']}">${settings['site.entries.title']}</a>
            </li>

            % for page in pages:
                % if page.slug != settings['site.home']:
                    <li><a href="/${page.slug}">${page.title}</a></li>
                % endif
            % endfor
        </ul>

        <h2 id="page-title">
            <%block name="page_title">Page Title Goes Here</%block>
        </h2>

        <%block name="flash">
            <% flash_messages = request.flash.pop('error') %>

            % if flash_messages:
                <ul class="flash error">
                    % for message in flash_messages:
                        <li>${message}</li>
                    % endfor
                </ul>
            % endif

            <% flash_messages = request.flash.pop() %>

            % if flash_messages:
                <ul class="flash">
                    % for message in flash_messages:
                        <li>${message}</li>
                    % endfor
                </ul>
            % endif
        </%block>

        <div id="content">
            <%block name="content">
                Content goes here
            </%block>
        </div>

        <%block name="bottom_nav"></%block>

        <footer>
            <%block name="footer">
                % if settings.get('site.copyright'):
                    <div id="copyright">&copy; ${settings['site.copyright'] | n}</div>
                % endif

                <div>
                    Powered by <a href="http://tangledframework.org/">tangled.web</a>
                </div>
            </%block>
        </footer>

        <%block name="javascripts">
            <!-- JavaScript tags go here -->
        </%block>
    </body>
</html>
