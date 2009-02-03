<?python 
  
  from textile                import textile
  from cgi                    import escape
?>
<div xmlns:py="http://purl.org/kid/ns#" id="recent-comments">
    <ol>
         <div py:strip="" py:for="comment in recent_comments">
              <li>
                  <small class="commentmetadata">
                  <a href="/${site.name}/blog/post/${comment.post.permalink}#comment_${comment.id}">
                      ${escape(comment.name)} 
                  </a>said 
                  
                  ${ XML(textile(escape(comment.short_text).encode('utf-8'), encoding='utf-8', output='utf-8')) }
                  </small>
              </li>
         </div>
    </ol>
</div>