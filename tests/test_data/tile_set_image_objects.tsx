<?xml version="1.0" encoding="UTF-8"?>
<tileset version="1.2" tiledversion="1.2.3" name="tile_set_image" tilewidth="32" tileheight="32" spacing="1" margin="1" tilecount="48" columns="8">
 <image source="images/tmw_desert_spacing.png" width="265" height="199"/>
 <tile id="9">
  <objectgroup draworder="index">
   <object id="2" name="wall" type="rectangle type" x="1" y="1" width="32" height="32" rotation="1"/>
  </objectgroup>
 </tile>
 <tile id="19">
  <objectgroup draworder="index">
   <object id="1" name="wall corner" type="polygon type" x="32" y="1" rotation="1">
    <polygon points="0,0 -32,0 -32,32 -16,32.1818 -15.8182,16.9091 0.181818,17.0909"/>
   </object>
  </objectgroup>
 </tile>
 <tile id="20">
  <objectgroup draworder="index">
   <object id="1" name="polyline" type="polyline type" x="1.45455" y="1.45455" rotation="1">
    <polyline points="0,0 25.0909,21.2727 9.63636,28.3636"/>
   </object>
  </objectgroup>
 </tile>
 <tile id="31">
  <objectgroup draworder="index">
   <object id="1" name="rock 1" type="elipse type" x="5.09091" y="2.54545" width="19.6364" height="19.2727" rotation="1">
    <ellipse/>
   </object>
   <object id="2" name="rock 2" type="elipse type" x="16.1818" y="22" width="8.54545" height="8.36364" rotation="-1">
    <ellipse/>
   </object>
  </objectgroup>
 </tile>
 <tile id="45">
  <objectgroup draworder="index">
   <object id="1" name="sign" type="point type" x="14.7273" y="26.3636">
    <point/>
   </object>
  </objectgroup>
 </tile>
</tileset>
