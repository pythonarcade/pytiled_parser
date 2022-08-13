<?xml version="1.0" encoding="UTF-8"?>
<tileset version="1.9" tiledversion="1.9.1" name="tileset" tilewidth="32" tileheight="32" tilecount="5" columns="0">
 <grid orientation="orthogonal" width="1" height="1"/>
 <tile id="0" class="tile">
  <properties>
   <property name="float property" type="float" value="2.2"/>
  </properties>
  <image width="32" height="32" source="../../images/tile_01.png"/>
  <animation>
   <frame tileid="0" duration="100"/>
   <frame tileid="1" duration="100"/>
   <frame tileid="2" duration="100"/>
   <frame tileid="3" duration="100"/>
  </animation>
 </tile>
 <tile id="1" class="tile">
  <properties>
   <property name="string property" value="testing"/>
  </properties>
  <image width="32" height="32" source="../../images/tile_02.png"/>
  <objectgroup draworder="index">
   <object id="2" x="13.4358" y="13.5305" width="14.4766" height="13.7197"/>
   <object id="3" x="13.8143" y="1.98699" width="14.2874" height="11.0704">
    <ellipse/>
   </object>
  </objectgroup>
 </tile>
 <tile id="2" class="tile">
  <properties>
   <property name="bool property" type="bool" value="true"/>
  </properties>
  <image width="32" height="32" source="../../images/tile_03.png"/>
 </tile>
 <tile id="3" class="tile">
  <image width="32" height="32" source="../../images/tile_04.png"/>
 </tile>
 <tile id="4" x="32" y="0" width="32" height="32">
  <image width="64" height="32" source="../../images/tile_05.png"/>
 </tile>
</tileset>
