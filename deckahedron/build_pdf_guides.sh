#! /bin/bash

pandoc --reference-odt=custom_pandoc_reference.odt mod_deckahedron_world.md -o /tmp/guide_player.odt
pandoc --reference-odt=custom_pandoc_reference.odt mod_deckahedron_world_gm_guide.md -o /tmp/guide_gm.odt
pandoc --reference-odt=custom_pandoc_reference.odt mod_deckahedron_world_campaigns.md -o /tmp/guide_campaigns.odt

cd dist

lowriter --headless --convert-to pdf /tmp/guide*.odt
