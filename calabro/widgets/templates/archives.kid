
<div xmlns:py="http://purl.org/kid/ns#" id="archives">
    <dl py:for="post in archive_posts">
      <dt><a href="/${site.name}/blog/archives/${post[7]}">${post[3].strftime('%B %Y')}</a></dt>
	  <dd>(${post[9]})</dd>
    </dl>
</div>