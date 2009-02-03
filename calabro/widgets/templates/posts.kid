<?python 
  
  from textile                import textile
  from cgi                    import escape
  
?>
<div xmlns:py="http://purl.org/kid/ns#" >
<div py:for="post in posts">
		<div id="post_$post.id">
				<div id="entry_$post.id">
					<div class="story">
						<h1><a py:content="post.title" href="/${site.name}/blog/post/${post.permalink}" /></h1>
						
					</div>
					<div class="entrybody">
				        <p>
			       			
			       			${ XML(textile(escape(post.text[:500]).encode('utf-8'), encoding='utf-8', output='utf-8'))} 
			       			
			       			<span py:if="len(post.text) > len(post.text[:500])">
			       			<a href="/${site.name}/blog/post/${post.permalink}">Continue reading...</a><br/><br/>
			       		    </span>
				        </p>
					</div>
					<div class="entrymeta">
						<div class="postinfo">
							<span class="postedby" py:content="post.posted_by()" /> 
							<span class="filedto"> on</span>
							<span class="posteddate" py:content="post.posted_date('%B %d, %Y')"/> |
							<span class="commentslink"><a href="/${site.name}/blog/post/${post.permalink}#comments">${post.number_of_comments()}</a></span> |
							<span class="filedto"> Filed under</span>
							<span py:for="tag in post.tags" >
								&nbsp;<a title='${tag.name}' href='/${site.name}/blog/tags/${tag.name}'>${tag.name}</a>
							</span>
						</div>
					
						<span py:if="'admin' in tg.identity.groups" class="commentslink"><a py:if="'admin' in tg.identity.groups" href="/${site.name}/blog/edit_post/${post.permalink}" >Edit</a></span>
					</div>
			   </div>
	    </div>
	    <br/>
</div >
</div>