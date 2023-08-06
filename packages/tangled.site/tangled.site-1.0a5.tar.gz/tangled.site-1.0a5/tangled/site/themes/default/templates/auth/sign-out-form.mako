<%def name="sign_out_form()">
    <form method="post" action="${request.make_path('/sign-out')}" class="sign-out-form">
        ${request.csrf_tag}
        <input type="submit" value="Sign Out">
    </form>
</%def>
