<?python 
  
  from textile                import textile
  from cgi                    import escape
?>
<li xmlns:py="http://purl.org/kid/ns#" class="alt"  id="comment_$comment.id"> 
	<small class="commentmetadata">
		<a href="${comment.web_site}"  >
		 ${escape(comment.name)}
		</a> 
		<span class="filedto"></span>
		<span class="posteddate" py:content="comment.posted_date('%B %d, %Y at %I:%M %p')"/>
	</small>
	<p >
		${ XML(textile(escape(comment.text).encode('utf-8'), encoding='utf-8', output='utf-8')) }

	</p>
</li>