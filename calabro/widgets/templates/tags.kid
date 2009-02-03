<?python

    def get_font_size(tag):
        if tag.count <= 3:
            count = 12
        elif tag.count <= 5:
            count = 15
        elif tag.count <= 7:
            count = 18
        elif tag.count <= 9:
            count = 20
        else:
            count = 24
        font = "%spx" % count 
        return font

?>

<div xmlns:py="http://purl.org/kid/ns#" id="tags">
    	<span py:for="tag in tags" style='font-size: ${get_font_size(tag)}'>  <a title='${tag.count}' href='/${site.name}/blog/tags/${tag.name}'>${tag.name}</a></span>
</div>