<%inherit file="base.mako"/>

<%block name="page_title">Edit Entry</%block>

<%block name="content">
    <form method="post" action="${request.resource_url('entry', {'id': entry.id})}">
        ${request.csrf_tag}
        <input type="hidden" name="$method" value="PUT">

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
                <input type="text" id="entry.slug" name="slug" value="${entry.slug}">
            </div>

            <div>
                <label for="entry.title">Title</label>
                <input type="text" id="entry.title" name="title" value="${entry.title}">
            </div>

            <div>
                <label for="entry.content">Content</label>
                <textarea id="entry.content" name="content">${entry.content}</textarea>
            </div>
        </div>

        <div class="buttons">
            <input type="submit" value="Update">
            <a href="${request.referer or request.application_url}">Cancel</a>
        </div>

        <hr>
    </form>

    <form method="post" action="${request.resource_url('entry', {'id': entry.id})}">
        ${request.csrf_tag}
        <input type="hidden" name="$method" value="DELETE">
        <div class="buttons">
            <input type="submit" value="Delete" class="danger">
        </div>
    </form>
</%block>
