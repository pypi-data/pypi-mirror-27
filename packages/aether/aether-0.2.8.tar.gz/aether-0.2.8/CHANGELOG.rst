Product Roadmap
===============

All product roadmap and notable changes to this project will be documented in this file.

[0.2a7] - 2017-12-15
--------------------

**Limitations:**

1) Search functionality is limited to one lat-lng polygon per search.
2) Search functionality will return only timestamps for which the polygon is entirely within the resource or satellite scene bounds, for instance, a LandSat scene.
3) Applications accessed via Sky require the input parameters to contain a polygon, and therefore have been written to make this input explicit to many Sky methods (e.g.,  Search, and those on AppSupportServices).

**Product Roadmap:**

*December 2017*

1) Search functionality to handle polygons that span Resource scenes. The query user interface will be amended to set a user-defined maximum time delta between neighboring scenes, e.g., within four days.
2) LandSat and Sentinel-2 Resources will add easily accessible bands for cloud, water, and ice detection derived their respective QA Bands. QA bands can already be accessed directly, but this will make access more user friendly.
3) Downloading and Search functionality will handle different geographic projections using GeoJSON and PyProj formats. 
4) Download functionality will transform from native reference system to requested reference system.
5) Lightning Quickstart python script to help new users search and download data, and run and build applications in minutes.
 
*Early January 2018*

1) Search functionality for multiple polygons (e.g., an equivalent of a GeoJSON Feature Collection).

*Late January 2018*

1) Addition of Javascript utilities library for posting embedded calls to Aether applications within web/mobile apps, and to search of Resources on behalf of web users.
2) Generalization of Sky application interface definition and the scope of application inputs.
