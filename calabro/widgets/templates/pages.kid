<div xmlns:py="http://purl.org/kid/ns#" id="pages">
	<ul py:for="page in pages">
		<li><a href="/${site.name}/page/${page.name}">${page.title}</a></li>
	</ul>
</div>