---
title: "An Analysis of Strange Timezones"
date: '2020-01-25'
excerpt: "Timezones are strange things. Be it Chatham Island's 45-minute offset or West Bank's ethnically divided use of daylight saving, it almost seems like the timezones of the world were chosen to baffle. In this post we ask which capital city has a timezone that differs the most from what would be expected given its longtitude. Any guesses?"
thumbnail: /gallery/thumbnails/strange-timezones.jpg
toc: false
categories:
- [Data Science, Visualisation]
tags:
- data-mining
- no-coding
- r
- story
---

{% colorquote info %}
This post is going to be code-free to make things easy to follow, but if you are interested in how I mined the data for this project and produced the final visualisation, you can find the code on this site's [GitHub repository](https://github.com/THargreaves/ttested).
{% endcolorquote %}


When I was younger, every summer my family and I would pack up our bags and take some time off to holiday in Spain. I can distinctly remember being interested in (and struggling to keep track of) the difference between the time in Spain and the one back home. It seemed strange that I found it so difficult to conceptualise this idea until one day it clicked: despite having flown in a net westward direction to reach our destination, we had somehow changed timezone in an easterly manner. How strange.

When we trace back the reasoning for this timezone choice (initiated in 1940 by Franco to align the country with Nazi Germany and Fascist Italy—his political allies) and consider the modern day benefits that the country might glean from being in line with its other western European neighbours, it doesn't seem unreasonable for things to be this way. If however, you were an alien visiting the Earth for a day lacking any historical, political or socio-economic context—it would seem like quite an odd decision.

## A Project is Born

Before I knew it, this train of thought was barreling down a hill with burnt-out brakes: "Which country has a timezone that differs the furthest from where it naturally should be based on longitude alone?".

The idea behind this is that in a perfect world (or more accurately, one where I'm in charge) timezones would be entirely dependent on the angle that a country makes with the prime meridian (the imaginary line passing through the Greenwich Royal Observatory). This would leave the UK with its current timezone of UTC+0 and then roughly one hour would be added for each 15 degrees traveled east and subtracted for west. Each country would then choose whichever timezone best matched up with its position.

Obviously such an approach would be impractical. It takes into account no ethnic divisions, political allegiances, or many other important factors. Furthermore, it's not clear how such a system would handle large (or to be exact, wide) countries. It would be ridiculous for a goliath such as Russia to share one common timezone. Despite these clear issues, I'm a mathematician and this is my hypothetical world, so tough luck.

With that aside, it begs the question of which countries' timezones would differ the most between the real world and my mathematically-pristine formulation. I decided to find out just that by scraping both timezone and longitudinal data from Wikipedia. The data represents all recognised countries for which their Wikipedia listings contained the information I required (which was most, but not all).

To simplify things slightly, I decided only to look at the capital city of each country and the timezone that it resides in. This way I didn't have to worry about the calculus of averaging population/land mass or looking at multiple timezones for one country. On top of this, I ignored daylight savings time, although this is probably for the best as it would skew large deviations of timezone towards countries which lie farther from the equator.

After performing the analysis, the twenty capitals whose timezone differed the most from my theoretical choice were as follows.


























![](/images/strange-timezones/strange-timezones_26_0.svg)


There you have it. The worse offending capital city is Rabat, Morocco with a whopping 1 hour 33 minute difference from what would be expected in a purely longitudinal system. The reason for this is that ever since 2018, Morocco has switched to permanently observing daylight saving time making UTC+1 its standard time despite virtually all of the country's landmass being farther west than even Plymouth.

As my younger self would have expected, Spain's Madrid comes out in a close second, 1 hour 15 minutes ahead off what would be expected. Even after these, there are still many countries with real-world timezones differing significantly from where they mathematically should align.

The really interesting observation is that every single one of these twenty worst offenders is ahead of its longitudinal timezone. I thought at first that this might have been a bug in my code and all differences had been converted to being positive. It turns out that this is not the case; there are capitals which fall behind their expected timezone. The five worse of those are shown below.








![](/images/strange-timezones/strange-timezones_33_0.svg)


These differences are noticeably smaller. My best guess is that most timezones are ahead of where they should be for the same reason that daylight saving exists—to offer more light in the morning. A colleague of mine suggested instead that it may be to do with the location of capital cities—do these tend to be more easterly? If you have any other suggestions please do let me know. For now, I will leave you with the finalised dataset to have a look through to find whichever country you fancy.





<script src="//ajax.googleapis.com/ajax/libs/jquery/1.9.1/jquery.min.js"></script>
<script >$(document).ready( function () {$('#table0').DataTable();} );</script>
<table id="table0" class="display">

<thead>
	<tr><th scope=col>capital</th><th scope=col>country</th><th scope=col>longitude</th><th scope=col>timezone</th><th scope=col>expected_timezone</th><th scope=col>timezone_diff</th></tr>
	<tr><th scope=col>&lt;chr&gt;</th><th scope=col>&lt;chr&gt;</th><th scope=col>&lt;dbl&gt;</th><th scope=col>&lt;dbl&gt;</th><th scope=col>&lt;dbl&gt;</th><th scope=col>&lt;dbl&gt;</th></tr>
</thead>
<tbody>
	<tr><td>Abu Dhabi                </td><td>United Arab Emirates            </td><td>  54.367000</td><td> 4.00</td><td>  3.62446667</td><td> 0.375533333</td></tr>
	<tr><td>Abuja                    </td><td>Nigeria                         </td><td>   7.483000</td><td> 1.00</td><td>  0.49886667</td><td> 0.501133333</td></tr>
	<tr><td>Accra                    </td><td>Ghana                           </td><td>  -0.200000</td><td> 0.00</td><td> -0.01333333</td><td> 0.013333333</td></tr>
	<tr><td>Addis Ababa              </td><td>Ethiopia                        </td><td>  38.740000</td><td> 3.00</td><td>  2.58266667</td><td> 0.417333333</td></tr>
	<tr><td>Algiers                  </td><td>Algeria                         </td><td>   3.058890</td><td> 1.00</td><td>  0.20392600</td><td> 0.796074000</td></tr>
	<tr><td>Amman                    </td><td>Jordan                          </td><td>  35.932780</td><td> 2.00</td><td>  2.39551867</td><td>-0.395518667</td></tr>
	<tr><td>Amsterdam                </td><td>Netherlands                     </td><td>   4.900000</td><td> 1.00</td><td>  0.32666667</td><td> 0.673333333</td></tr>
	<tr><td>Ankara                   </td><td>Turkey                          </td><td>  32.867000</td><td> 3.00</td><td>  2.19113333</td><td> 0.808866667</td></tr>
	<tr><td>Antananarivo             </td><td>Madagascar                      </td><td>  47.517000</td><td> 3.00</td><td>  3.16780000</td><td>-0.167800000</td></tr>
	<tr><td>Apia                     </td><td>Samoa                           </td><td>-171.750000</td><td>13.00</td><td>-11.45000000</td><td> 0.450000000</td></tr>
	<tr><td>Ashgabat                 </td><td>Turkmenistan                    </td><td>  58.367000</td><td> 5.00</td><td>  3.89113333</td><td> 1.108866667</td></tr>
	<tr><td>Asmara                   </td><td>Eritrea                         </td><td>  38.925000</td><td> 3.00</td><td>  2.59500000</td><td> 0.405000000</td></tr>
	<tr><td>Athens                   </td><td>Greece                          </td><td>  23.727806</td><td> 2.00</td><td>  1.58185373</td><td> 0.418146267</td></tr>
	<tr><td>Baghdad                  </td><td>Iraq                            </td><td>  44.383000</td><td> 3.00</td><td>  2.95886667</td><td> 0.041133333</td></tr>
	<tr><td>Baku                     </td><td>Azerbaijan                      </td><td>  49.882220</td><td> 4.00</td><td>  3.32548133</td><td> 0.674518667</td></tr>
	<tr><td>Bamako                   </td><td>Mali                            </td><td>  -8.002780</td><td> 0.00</td><td> -0.53351867</td><td> 0.533518667</td></tr>
	<tr><td>Bandar Seri Begawan      </td><td>Brunei                          </td><td> 114.942220</td><td> 8.00</td><td>  7.66281467</td><td> 0.337185333</td></tr>
	<tr><td>Bangkok                  </td><td>Thailand                        </td><td> 100.494170</td><td> 7.00</td><td>  6.69961133</td><td> 0.300388667</td></tr>
	<tr><td>Banjul                   </td><td>Gambia                          </td><td> -16.577500</td><td> 0.00</td><td> -1.10516667</td><td> 1.105166667</td></tr>
	<tr><td>Basseterre               </td><td>Saint Kitts and Nevis           </td><td> -62.733000</td><td>-4.00</td><td> -4.18220000</td><td> 0.182200000</td></tr>
	<tr><td>Beijing                  </td><td>China                           </td><td> 116.383000</td><td> 8.00</td><td>  7.75886667</td><td> 0.241133333</td></tr>
	<tr><td>Beirut                   </td><td>Lebanon                         </td><td>  35.513060</td><td> 2.00</td><td>  2.36753733</td><td>-0.367537333</td></tr>
	<tr><td>Belgrade                 </td><td>Serbia                          </td><td>  20.467000</td><td> 1.00</td><td>  1.36446667</td><td>-0.364466667</td></tr>
	<tr><td>Belmopan                 </td><td>Belize                          </td><td> -88.766940</td><td>-6.00</td><td> -5.91779600</td><td>-0.082204000</td></tr>
	<tr><td>Berlin                   </td><td>Germany                         </td><td>  13.405000</td><td> 1.00</td><td>  0.89366667</td><td> 0.106333333</td></tr>
	<tr><td>Bishkek                  </td><td>Kyrgyzstan                      </td><td>  74.612220</td><td> 6.00</td><td>  4.97414800</td><td> 1.025852000</td></tr>
	<tr><td>Bogotá                   </td><td>Colombia                        </td><td> -74.072220</td><td>-5.00</td><td> -4.93814800</td><td>-0.061852000</td></tr>
	<tr><td>Brasília                 </td><td>Brazil                          </td><td> -47.882780</td><td>-3.00</td><td> -3.19218533</td><td> 0.192185333</td></tr>
	<tr><td>Bratislava               </td><td>Slovakia                        </td><td>  17.109720</td><td> 1.00</td><td>  1.14064800</td><td>-0.140648000</td></tr>
	<tr><td>Bridgetown               </td><td>Barbados                        </td><td> -59.616670</td><td>-4.00</td><td> -3.97444467</td><td>-0.025555333</td></tr>
	<tr><td>Bucharest                </td><td>Romania                         </td><td>  26.103890</td><td> 2.00</td><td>  1.74025933</td><td> 0.259740667</td></tr>
	<tr><td>Budapest                 </td><td>Hungary                         </td><td>  19.051390</td><td> 1.00</td><td>  1.27009267</td><td>-0.270092667</td></tr>
	<tr><td>Buenos Aires             </td><td>Argentina                       </td><td> -58.381670</td><td>-3.00</td><td> -3.89211133</td><td> 0.892111333</td></tr>
	<tr><td>Cairo                    </td><td>Egypt                           </td><td>  31.233000</td><td> 2.00</td><td>  2.08220000</td><td>-0.082200000</td></tr>
	<tr><td>Caracas                  </td><td>Venezuela                       </td><td> -66.903610</td><td>-4.00</td><td> -4.46024067</td><td> 0.460240667</td></tr>
	<tr><td>Castries                 </td><td>Saint Lucia                     </td><td> -60.983000</td><td>-4.00</td><td> -4.06553333</td><td> 0.065533333</td></tr>
	<tr><td><span style=white-space:pre-wrap>Chi&lt;U+0219&gt;inau          </span></td><td><span style=white-space:pre-wrap>Moldova                         </span></td><td><span style=white-space:pre-wrap>  28.835335</span></td><td> 2.00</td><td><span style=white-space:pre-wrap>  1.92235567</span></td><td> 0.077644333</td></tr>
	<tr><td>Conakry                  </td><td>Guinea                          </td><td> -13.712220</td><td> 0.00</td><td> -0.91414800</td><td> 0.914148000</td></tr>
	<tr><td>Copenhagen               </td><td>Denmark                         </td><td>  12.568330</td><td> 1.00</td><td>  0.83788867</td><td> 0.162111333</td></tr>
	<tr><td>Dakar                    </td><td>Senegal                         </td><td> -17.446670</td><td> 0.00</td><td> -1.16311133</td><td> 1.163111333</td></tr>
	<tr><td>Damascus                 </td><td>Syria                           </td><td>  36.291940</td><td> 2.00</td><td>  2.41946267</td><td>-0.419462667</td></tr>
	<tr><td>Dhaka                    </td><td>Bangladesh                      </td><td>  90.388890</td><td> 6.00</td><td>  6.02592600</td><td>-0.025926000</td></tr>
	<tr><td>Dili                     </td><td>East Timor                      </td><td> 125.567000</td><td> 9.00</td><td>  8.37113333</td><td> 0.628866667</td></tr>
	<tr><td>Djibouti                 </td><td>Djibouti                        </td><td>  43.145000</td><td> 3.00</td><td>  2.87633333</td><td> 0.123666667</td></tr>
	<tr><td>Dodoma                   </td><td>Tanzania                        </td><td>  35.741940</td><td> 3.00</td><td>  2.38279600</td><td> 0.617204000</td></tr>
	<tr><td>Doha                     </td><td>Qatar                           </td><td>  51.533330</td><td> 3.00</td><td>  3.43555533</td><td>-0.435555333</td></tr>
	<tr><td>Dublin                   </td><td>Ireland                         </td><td>  -6.267000</td><td> 0.00</td><td> -0.41780000</td><td> 0.417800000</td></tr>
	<tr><td>Dushanbe                 </td><td>Tajikistan                      </td><td>  68.780000</td><td> 5.00</td><td>  4.58533333</td><td> 0.414666667</td></tr>
	<tr><td>Gaborone                 </td><td>Botswana                        </td><td>  25.912220</td><td> 2.00</td><td>  1.72748133</td><td> 0.272518667</td></tr>
	<tr><td>Georgetown               </td><td>Guyana                          </td><td> -58.155280</td><td>-4.00</td><td> -3.87701867</td><td>-0.122981333</td></tr>
	<tr><td>Guatemala City           </td><td>Guatemala                       </td><td> -90.535280</td><td>-6.00</td><td> -6.03568533</td><td> 0.035685333</td></tr>
	<tr><td>Hanoi                    </td><td>Vietnam                         </td><td> 105.854170</td><td> 7.00</td><td>  7.05694467</td><td>-0.056944667</td></tr>
	<tr><td>Harare                   </td><td>Zimbabwe                        </td><td>  31.052220</td><td> 2.00</td><td>  2.07014800</td><td>-0.070148000</td></tr>
	<tr><td>Havana                   </td><td>Cuba                            </td><td> -82.358890</td><td>-5.00</td><td> -5.49059267</td><td> 0.490592667</td></tr>
	<tr><td>Helsinki                 </td><td>Finland                         </td><td>  24.937500</td><td> 2.00</td><td>  1.66250000</td><td> 0.337500000</td></tr>
	<tr><td>Honiara                  </td><td>Solomon Islands                 </td><td> 159.955560</td><td>11.00</td><td> 10.66370400</td><td> 0.336296000</td></tr>
	<tr><td>Islamabad                </td><td>Pakistan                        </td><td>  73.063890</td><td> 5.00</td><td>  4.87092600</td><td> 0.129074000</td></tr>
	<tr><td>Jakarta                  </td><td>Indonesia                       </td><td> 106.817000</td><td> 7.00</td><td>  7.12113333</td><td>-0.121133333</td></tr>
	<tr><td>Jerusalem                </td><td>Israel                          </td><td>  35.217000</td><td> 2.00</td><td>  2.34780000</td><td>-0.347800000</td></tr>
	<tr><td>Jerusalem                </td><td>Palestine                       </td><td>  35.217000</td><td> 2.00</td><td>  2.34780000</td><td>-0.347800000</td></tr>
	<tr><td>Juba                     </td><td>South Sudan                     </td><td>  31.600000</td><td> 3.00</td><td>  2.10666667</td><td> 0.893333333</td></tr>
	<tr><td>Kabul                    </td><td>Afghanistan                     </td><td>  69.178330</td><td> 4.50</td><td>  4.61188867</td><td>-0.111888667</td></tr>
	<tr><td>Kampala                  </td><td>Uganda                          </td><td>  32.581110</td><td> 3.00</td><td>  2.17207400</td><td> 0.827926000</td></tr>
	<tr><td>Kathmandu                </td><td>Nepal                           </td><td>  85.267000</td><td> 5.75</td><td>  5.68446667</td><td> 0.065533333</td></tr>
	<tr><td>Khartoum                 </td><td>Sudan                           </td><td>  32.560000</td><td> 2.00</td><td>  2.17066667</td><td>-0.170666667</td></tr>
	<tr><td>Kiev                     </td><td>Ukraine                         </td><td>  30.523330</td><td> 2.00</td><td>  2.03488867</td><td>-0.034888667</td></tr>
	<tr><td>Kigali                   </td><td>Rwanda                          </td><td>  30.059440</td><td> 2.00</td><td>  2.00396267</td><td>-0.003962667</td></tr>
	<tr><td>Kingston                 </td><td>Jamaica                         </td><td> -76.793060</td><td>-5.00</td><td> -5.11953733</td><td> 0.119537333</td></tr>
	<tr><td>Kingstown                </td><td>Saint Vincent and the Grenadines</td><td> -61.225000</td><td>-4.00</td><td> -4.08166667</td><td> 0.081666667</td></tr>
	<tr><td>Kuala Lumpur             </td><td>Malaysia                        </td><td> 101.695280</td><td> 8.00</td><td>  6.77968533</td><td> 1.220314667</td></tr>
	<tr><td>Kuwait City              </td><td>Kuwait                          </td><td>  47.978330</td><td> 3.00</td><td>  3.19855533</td><td>-0.198555333</td></tr>
	<tr><td>Lilongwe                 </td><td>Malawi                          </td><td>  33.783000</td><td> 2.00</td><td>  2.25220000</td><td>-0.252200000</td></tr>
	<tr><td>Lima                     </td><td>Peru                            </td><td> -77.033000</td><td>-5.00</td><td> -5.13553333</td><td> 0.135533333</td></tr>
	<tr><td>Lisbon                   </td><td>Portugal                        </td><td>  -9.150019</td><td> 0.00</td><td> -0.61000129</td><td> 0.610001287</td></tr>
	<tr><td>Ljubljana                </td><td>Slovenia                        </td><td>  14.508330</td><td> 1.00</td><td>  0.96722200</td><td> 0.032778000</td></tr>
	<tr><td>Lomé                     </td><td>Togo                            </td><td>   1.222780</td><td> 0.00</td><td>  0.08151867</td><td>-0.081518667</td></tr>
	<tr><td>London                   </td><td>United Kingdom                  </td><td>  -0.127500</td><td> 0.00</td><td> -0.00850000</td><td> 0.008500000</td></tr>
	<tr><td>Lusaka                   </td><td>Zambia                          </td><td>  28.283000</td><td> 2.00</td><td>  1.88553333</td><td> 0.114466667</td></tr>
	<tr><td>Luxembourg               </td><td>Luxembourg                      </td><td>   6.131940</td><td> 1.00</td><td>  0.40879600</td><td> 0.591204000</td></tr>
	<tr><td>Madrid                   </td><td>Spain                           </td><td>  -3.717000</td><td> 1.00</td><td> -0.24780000</td><td> 1.247800000</td></tr>
	<tr><td>Majuro                   </td><td>Marshall Islands                </td><td> 171.383000</td><td>12.00</td><td> 11.42553333</td><td> 0.574466667</td></tr>
	<tr><td>Malabo                   </td><td>Equatorial Guinea               </td><td>   8.783000</td><td> 1.00</td><td>  0.58553333</td><td> 0.414466667</td></tr>
	<tr><td>Malé                     </td><td>Maldives                        </td><td>  73.508890</td><td> 5.00</td><td>  4.90059267</td><td> 0.099407333</td></tr>
	<tr><td>Managua                  </td><td>Nicaragua                       </td><td> -86.251390</td><td>-6.00</td><td> -5.75009267</td><td>-0.249907333</td></tr>
	<tr><td>Manila                   </td><td>Philippines                     </td><td> 120.977200</td><td> 8.00</td><td>  8.06514667</td><td>-0.065146667</td></tr>
	<tr><td>Maputo                   </td><td>Mozambique                      </td><td>  32.583000</td><td> 2.00</td><td>  2.17220000</td><td>-0.172200000</td></tr>
	<tr><td>Maseru                   </td><td>Lesotho                         </td><td>  27.480000</td><td> 2.00</td><td>  1.83200000</td><td> 0.168000000</td></tr>
	<tr><td>Mexico City              </td><td>Mexico                          </td><td> -99.133000</td><td>-6.00</td><td> -6.60886667</td><td> 0.608866667</td></tr>
	<tr><td>Minsk                    </td><td>Belarus                         </td><td>  27.567000</td><td> 3.00</td><td>  1.83780000</td><td> 1.162200000</td></tr>
	<tr><td>Mogadishu                </td><td>Somalia                         </td><td>  45.333000</td><td> 3.00</td><td>  3.02220000</td><td>-0.022200000</td></tr>
	<tr><td>Monaco                   </td><td>Monaco                          </td><td>   7.417000</td><td> 1.00</td><td>  0.49446667</td><td> 0.505533333</td></tr>
	<tr><td>Monrovia                 </td><td>Liberia                         </td><td> -10.801390</td><td> 0.00</td><td> -0.72009267</td><td> 0.720092667</td></tr>
	<tr><td>Montevideo               </td><td>Uruguay                         </td><td> -56.181940</td><td>-3.00</td><td> -3.74546267</td><td> 0.745462667</td></tr>
	<tr><td>Moroni                   </td><td>Comoros                         </td><td>  43.256000</td><td> 3.00</td><td>  2.88373333</td><td> 0.116266667</td></tr>
	<tr><td>Moscow                   </td><td>Russia                          </td><td>  37.617000</td><td> 3.00</td><td>  2.50780000</td><td> 0.492200000</td></tr>
	<tr><td>Muscat                   </td><td>Oman                            </td><td>  58.408330</td><td> 4.00</td><td>  3.89388867</td><td> 0.106111333</td></tr>
	<tr><td>Nairobi                  </td><td>Kenya                           </td><td>  36.817220</td><td> 3.00</td><td>  2.45448133</td><td> 0.545518667</td></tr>
	<tr><td>Nassau                   </td><td>Bahamas                         </td><td> -77.345000</td><td>-5.00</td><td> -5.15633333</td><td> 0.156333333</td></tr>
	<tr><td>Naypyidaw                </td><td>Myanmar                         </td><td>  96.100000</td><td> 6.50</td><td>  6.40666667</td><td> 0.093333333</td></tr>
	<tr><td>New Delhi                </td><td>India                           </td><td>  77.208890</td><td> 5.50</td><td>  5.14725933</td><td> 0.352740667</td></tr>
	<tr><td>Ngerulmud                </td><td>Palau                           </td><td> 134.624170</td><td> 9.00</td><td>  8.97494467</td><td> 0.025055333</td></tr>
	<tr><td>Niamey                   </td><td>Niger                           </td><td>   2.125280</td><td> 1.00</td><td>  0.14168533</td><td> 0.858314667</td></tr>
	<tr><td>Nicosia                  </td><td>Cyprus                          </td><td>  33.365000</td><td> 2.00</td><td>  2.22433333</td><td>-0.224333333</td></tr>
	<tr><td><span style=white-space:pre-wrap>Nuku&lt;U+02BB&gt;alofa        </span></td><td><span style=white-space:pre-wrap>Tonga                           </span></td><td>-175.200000</td><td>13.00</td><td>-11.68000000</td><td> 0.680000000</td></tr>
	<tr><td>Nur-Sultan               </td><td>Kazakhstan                      </td><td>  71.433000</td><td> 6.00</td><td>  4.76220000</td><td> 1.237800000</td></tr>
	<tr><td>Oslo                     </td><td>Norway                          </td><td>  10.733330</td><td> 1.00</td><td>  0.71555533</td><td> 0.284444667</td></tr>
	<tr><td>Ottawa                   </td><td>Canada                          </td><td> -75.695000</td><td>-5.00</td><td> -5.04633333</td><td> 0.046333333</td></tr>
	<tr><td>Ouagadougou              </td><td>Burkina Faso                    </td><td>  -1.535280</td><td> 0.00</td><td> -0.10235200</td><td> 0.102352000</td></tr>
	<tr><td>Palikir                  </td><td>Federated States of Micronesia  </td><td> 158.158890</td><td>11.00</td><td> 10.54392600</td><td> 0.456074000</td></tr>
	<tr><td>Paramaribo               </td><td>Suriname                        </td><td> -55.203890</td><td>-3.00</td><td> -3.68025933</td><td> 0.680259333</td></tr>
	<tr><td>Paris                    </td><td>France                          </td><td>   2.352222</td><td> 1.00</td><td>  0.15681480</td><td> 0.843185200</td></tr>
	<tr><td>Phnom Penh               </td><td>Cambodia                        </td><td> 104.921110</td><td> 7.00</td><td>  6.99474067</td><td> 0.005259333</td></tr>
	<tr><td>Podgorica                </td><td>Montenegro                      </td><td>  19.262892</td><td> 1.00</td><td>  1.28419278</td><td>-0.284192780</td></tr>
	<tr><td>Port Louis               </td><td>Mauritius                       </td><td>  57.504170</td><td> 4.00</td><td>  3.83361133</td><td> 0.166388667</td></tr>
	<tr><td>Port Moresby             </td><td>Papua New Guinea                </td><td> 147.149440</td><td>10.00</td><td>  9.80996267</td><td> 0.190037333</td></tr>
	<tr><td>Port Vila                </td><td>Vanuatu                         </td><td> 168.317000</td><td>11.00</td><td> 11.22113333</td><td>-0.221133333</td></tr>
	<tr><td>Port-au-Prince           </td><td>Haiti                           </td><td> -72.333000</td><td>-5.00</td><td> -4.82220000</td><td>-0.177800000</td></tr>
	<tr><td>Port of Spain            </td><td>Trinidad and Tobago             </td><td> -61.517000</td><td>-4.00</td><td> -4.10113333</td><td> 0.101133333</td></tr>
	<tr><td>Prague                   </td><td>Czech Republic                  </td><td>  14.417000</td><td> 1.00</td><td>  0.96113333</td><td> 0.038866667</td></tr>
	<tr><td>Pretoria                 </td><td>South Africa                    </td><td>  28.188060</td><td> 2.00</td><td>  1.87920400</td><td> 0.120796000</td></tr>
	<tr><td>Pyongyang                </td><td>North Korea                     </td><td> 125.738060</td><td> 9.00</td><td>  8.38253733</td><td> 0.617462667</td></tr>
	<tr><td>Quito                    </td><td>Ecuador                         </td><td> -78.517000</td><td>-5.00</td><td> -5.23446667</td><td> 0.234466667</td></tr>
	<tr><td>Rabat                    </td><td>Morocco                         </td><td>  -6.841650</td><td> 1.00</td><td> -0.45611000</td><td> 1.456110000</td></tr>
	<tr><td>Riga                     </td><td>Latvia                          </td><td>  24.106390</td><td> 2.00</td><td>  1.60709267</td><td> 0.392907333</td></tr>
	<tr><td>Riyadh                   </td><td>Saudi Arabia                    </td><td>  46.717000</td><td> 3.00</td><td>  3.11446667</td><td>-0.114466667</td></tr>
	<tr><td>Rome                     </td><td>Italy                           </td><td>  12.500000</td><td> 1.00</td><td>  0.83333333</td><td> 0.166666667</td></tr>
	<tr><td>San José                 </td><td>Costa Rica                      </td><td> -84.083000</td><td>-6.00</td><td> -5.60553333</td><td>-0.394466667</td></tr>
	<tr><td>San Marino               </td><td>San Marino                      </td><td>  12.447300</td><td> 1.00</td><td>  0.82982000</td><td> 0.170180000</td></tr>
	<tr><td>San Salvador             </td><td>El Salvador                     </td><td> -89.191390</td><td>-6.00</td><td> -5.94609267</td><td>-0.053907333</td></tr>
	<tr><td>Sana'a                   </td><td>Yemen                           </td><td>  44.206390</td><td> 3.00</td><td>  2.94709267</td><td> 0.052907333</td></tr>
	<tr><td>Santiago                 </td><td>Chile                           </td><td> -70.667000</td><td>-4.00</td><td> -4.71113333</td><td> 0.711133333</td></tr>
	<tr><td>São Tomé                 </td><td>São Tomé and Príncipe           </td><td>   6.730560</td><td> 0.00</td><td>  0.44870400</td><td>-0.448704000</td></tr>
	<tr><td>Sarajevo                 </td><td>Bosnia and Herzegovina          </td><td>  18.417000</td><td> 1.00</td><td>  1.22780000</td><td>-0.227800000</td></tr>
	<tr><td>Singapore                </td><td>Singapore                       </td><td> 103.833000</td><td> 8.00</td><td>  6.92220000</td><td> 1.077800000</td></tr>
	<tr><td>Skopje                   </td><td>North Macedonia                 </td><td>  21.433000</td><td> 1.00</td><td>  1.42886667</td><td>-0.428866667</td></tr>
	<tr><td>Sofia                    </td><td>Bulgaria                        </td><td>  23.330000</td><td> 2.00</td><td>  1.55533333</td><td> 0.444666667</td></tr>
	<tr><td>Sri Jayawardenepura Kotte</td><td>Sri Lanka                       </td><td>  79.887836</td><td> 5.50</td><td>  5.32585574</td><td> 0.174144260</td></tr>
	<tr><td>St. George's             </td><td>Grenada                         </td><td> -61.750000</td><td>-4.00</td><td> -4.11666667</td><td> 0.116666667</td></tr>
	<tr><td>St. John's               </td><td>Antigua and Barbuda             </td><td> -61.850000</td><td>-4.00</td><td> -4.12333333</td><td> 0.123333333</td></tr>
	<tr><td>Stockholm                </td><td>Sweden                          </td><td>  18.068610</td><td> 1.00</td><td>  1.20457400</td><td>-0.204574000</td></tr>
	<tr><td>Sucre                    </td><td>Bolivia                         </td><td> -65.250000</td><td>-4.00</td><td> -4.35000000</td><td> 0.350000000</td></tr>
	<tr><td>Suva                     </td><td>Fiji                            </td><td> 178.441900</td><td>12.00</td><td> 11.89612667</td><td> 0.103873333</td></tr>
	<tr><td>Tallinn                  </td><td>Estonia                         </td><td>  24.745280</td><td> 2.00</td><td>  1.64968533</td><td> 0.350314667</td></tr>
	<tr><td>Tashkent                 </td><td>Uzbekistan                      </td><td>  69.267000</td><td> 5.00</td><td>  4.61780000</td><td> 0.382200000</td></tr>
	<tr><td>Tbilisi                  </td><td>Georgia                         </td><td>  44.783000</td><td> 4.00</td><td>  2.98553333</td><td> 1.014466667</td></tr>
	<tr><td>Tegucigalpa              </td><td>Honduras                        </td><td> -87.217000</td><td>-6.00</td><td> -5.81446667</td><td>-0.185533333</td></tr>
	<tr><td>Tehran                   </td><td>Iran                            </td><td>  51.388890</td><td> 3.50</td><td>  3.42592600</td><td> 0.074074000</td></tr>
	<tr><td>Thimphu                  </td><td>Bhutan                          </td><td>  89.636110</td><td> 6.00</td><td>  5.97574067</td><td> 0.024259333</td></tr>
	<tr><td>Tokyo                    </td><td>Japan                           </td><td> 139.692220</td><td> 9.00</td><td>  9.31281467</td><td>-0.312814667</td></tr>
	<tr><td>Tripoli                  </td><td>Libya                           </td><td>  13.191390</td><td> 2.00</td><td>  0.87942600</td><td> 1.120574000</td></tr>
	<tr><td>Tunis                    </td><td>Tunisia                         </td><td>  10.181670</td><td> 1.00</td><td>  0.67877800</td><td> 0.321222000</td></tr>
	<tr><td>Ulaanbaatar              </td><td>Mongolia                        </td><td> 106.917220</td><td> 8.00</td><td>  7.12781467</td><td> 0.872185333</td></tr>
	<tr><td>Vaduz                    </td><td>Liechtenstein                   </td><td>   9.521000</td><td> 1.00</td><td>  0.63473333</td><td> 0.365266667</td></tr>
	<tr><td>Valletta                 </td><td>Malta                           </td><td>  14.506940</td><td> 1.00</td><td>  0.96712933</td><td> 0.032870667</td></tr>
	<tr><td>Vatican City             </td><td>Vatican City                    </td><td>  12.452500</td><td> 1.00</td><td>  0.83016667</td><td> 0.169833333</td></tr>
	<tr><td>Vienna                   </td><td>Austria                         </td><td>  16.367000</td><td> 1.00</td><td>  1.09113333</td><td>-0.091133333</td></tr>
	<tr><td>Vientiane                </td><td>Laos                            </td><td> 102.600000</td><td> 7.00</td><td>  6.84000000</td><td> 0.160000000</td></tr>
	<tr><td>Vilnius                  </td><td>Lithuania                       </td><td>  25.283000</td><td> 2.00</td><td>  1.68553333</td><td> 0.314466667</td></tr>
	<tr><td>Warsaw                   </td><td>Poland                          </td><td>  21.017000</td><td> 1.00</td><td>  1.40113333</td><td>-0.401133333</td></tr>
	<tr><td>Washington, D.C.         </td><td>United States                   </td><td> -77.016390</td><td>-5.00</td><td> -5.13442600</td><td> 0.134426000</td></tr>
	<tr><td>Wellington               </td><td>New Zealand                     </td><td> 174.777220</td><td>12.00</td><td> 11.65181467</td><td> 0.348185333</td></tr>
	<tr><td>Windhoek                 </td><td>Namibia                         </td><td>  17.083610</td><td> 2.00</td><td>  1.13890733</td><td> 0.861092667</td></tr>
	<tr><td>Yamoussoukro             </td><td>Ivory Coast                     </td><td>  -5.283000</td><td> 0.00</td><td> -0.35220000</td><td> 0.352200000</td></tr>
	<tr><td>Yaoundé                  </td><td>Cameroon                        </td><td>  11.517000</td><td> 1.00</td><td>  0.76780000</td><td> 0.232200000</td></tr>
	<tr><td>Yaren                    </td><td>Nauru                           </td><td> 166.920867</td><td>12.00</td><td> 11.12805778</td><td> 0.871942220</td></tr>
	<tr><td>Yerevan                  </td><td>Armenia                         </td><td>  44.514440</td><td> 4.00</td><td>  2.96762933</td><td> 1.032370667</td></tr>
	<tr><td>Zagreb                   </td><td>Croatia                         </td><td>  15.983000</td><td> 1.00</td><td>  1.06553333</td><td>-0.065533333</td></tr>
</tbody>
</table>


