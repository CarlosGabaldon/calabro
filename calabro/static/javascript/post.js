function add_comment() {
    var post_id = $('post_id').value;
    var name = $('new_comment_name').value;
    var web_site = $('new_comment_web_site').value;
    var email = $('new_comment_email').value;
    var text = $('new_comment_text').value;
    var site = $('site_name').value;

    var data = { 'post_id'  : post_id,
                 'name'     : name,
                 'web_site' : web_site,
                 'email'    : email,
                 'text'  : text };
                 
    var url = '/' + site + '/blog/create_comment?' + queryString(data);
    
    new Ajax.Updater(
                     'commentlist',
                     url,
                    {
                        method:'get',
                        asynchronous:true, 
                        insertion: Insertion.Bottom 
                    }
                  );
                  
    url = '/' + site + '/blog/comment_count?post_id=' + post_id;
    
    new Ajax.Request(
                    url,
                    {
                        method:'get',
                        onSuccess: function(transport) 
                        {
                            $('comments').innerHTML = transport.responseText;
                 
                        } 
                    }
                 );
           
     
    $('new_comment-form').reset();
    
}

function live_search(value, site){
    
    var query = value;
    
    if (query == "") return;    
    
    url = '/' + site + '/blog/search';
    
    new Ajax.Updater(
                     'posts',
                     url,
                    {
                        method:'post',
                        asynchronous:true,
                        parameters: 'query=' + query
                    }
                  );
    
}


function add_badge() {
    var site_id = $('site_id').value;
    var name = $('new_badge_name').value;
    var html = $('new_badge_html').value;
    var site = $('site_name').value;

    var data = { 'site_id'  : site_id,
                 'name'     : name,
                 'html'     : html };
                 
    var url = '/' + site + '/site/create_badge?' + queryString(data);
    
    new Ajax.Updater(
                     'badgelist',
                     url,
                    {
                        method:'get',
                        asynchronous:true, 
                        insertion: Insertion.Bottom 
                    }
                  );
                  
    $('new_badge-form').reset();
    
}