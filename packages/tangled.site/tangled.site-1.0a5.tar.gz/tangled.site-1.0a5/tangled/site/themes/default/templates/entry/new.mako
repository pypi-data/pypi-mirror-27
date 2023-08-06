<%inherit file="base.mako"/>

<%block name="page_title">New Entry</%block>

<%block name="content">
    <form method="post" action="${request.make_path('/entries')}">
        ${request.csrf_tag}

        <div class="column">
            <label>
                <input type="checkbox" id="entry.published" name="published"
                        ${'checked' if entry.published else ''}>
                Published?
            </label>

            <label>
                <input type="checkbox" id="entry.is_page" name="is_page"
                       ${'checked' if entry.is_page else ''}>
                Page?
            </label>

            <div>
                <label for="entry.slug">Slug</label>
                <input type="text" id="entry.slug" name="slug">
            </div>

            <div>
                <label for="entry.title">Title</label>
                <input type="text" id="entry.title" name="title">
            </div>

            <div>
                <label for="entry.content">Content</label>
                <textarea id="entry.content" name="content"></textarea>
            </div>
        </div>

        <div class="buttons">
            <input type="submit" value="Create new entry">
            <a href="${request.referer or request.application_url}">Cancel</a>
        </div>
    </form>
</%block>
