<div  xmlns:py="http://purl.org/kid/ns#" >
    <div  id="admin" py:if="tg.identity.anonymous">
    	Welcome, guest,
    	<a href='/${site.name}/site/login'>login</a>
    	<p/>

     </div>
     <div id="admin" py:if="not tg.identity.anonymous">
    	Welcome, ${tg.identity.user.display_name},
    	<a href='/${site.name}/site/logout'>logout</a>
    	<p/>
     </div>
     <div id="admin" py:if="'admin' in tg.identity.groups">
         <h1>administer your site</h1>
             <dl>
               <dt>New Post:</dt>
               <dd><a href="/${site.name}/blog/new_post">Create</a></dd>
               <dt>New Page:</dt>
               <dd><a href="/${site.name}/page/new_page">Create</a></dd>
               <dt>New User:</dt>
               <dd><a href="/${site.name}/users/new">Create</a></dd>
    			<dt>Edit Site:</dt>
               <dd><a href="/${site.name}/site/edit_site">Edit</a></dd>
               <dt>New Site:</dt>
               <dd><a href="/${site.name}/site/new_site">Create</a></dd>
             </dl>              
     </div>
 </div>