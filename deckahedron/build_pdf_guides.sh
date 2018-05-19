#! /bin/bash

cp ./markdown.css /tmp/markdown.css

 #-s                puts the utf-8 header in
 #--self-contained  puts data: URLs in
 #-t html           to HTML
pandoc \
 -s \
 --self-contained \
 -t html \
 --css=/tmp/markdown.css \
 mod_deckahedron_world_gm_guide.md -o /tmp/guide_gm.html

pandoc --reference-odt=custom_pandoc_reference.odt mod_deckahedron_world.md -o /tmp/guide_player.odt
pandoc --reference-odt=custom_pandoc_reference.odt mod_deckahedron_world_gm_guide.md -o /tmp/guide_gm.odt
pandoc --reference-odt=custom_pandoc_reference.odt mod_deckahedron_world_campaigns.md -o /tmp/guide_campaigns.odt

cd dist

lowriter --headless --convert-to pdf /tmp/guide*.odt


