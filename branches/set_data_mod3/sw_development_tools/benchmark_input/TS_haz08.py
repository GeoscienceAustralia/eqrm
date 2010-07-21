"""
  EQRM parameter file

  All input files are first searched for in the input_dir, then in the
  resources/data directory, which is part of EQRM.

 All distances are in kilometers.
 Acceleration values are in g.
 Angles, latitude and longitude are in decimal degrees.

 If a field is not used, set the value to None.


"""

from eqrm_code.parse_in_parameters import eqrm_data_home, get_time_user
from os.path import join


# Operation Mode
run_type = "hazard" 
is_scenario = False
max_width = 15

# Scenario input
scenario_azimith = 340
scenario_depth = 11.5
scenario_latitude = -32.95
scenario_longitude = 151.61
scenario_magnitude = 5.6
scenario_number_of_events = 2

# Probabilistic input
prob_azimuth_in_zones = [180, 180, 180, 180, 180, 180]
prob_delta_azimuth_in_zones = [180, 180, 180, 180, 180, 180]
prob_min_mag_cutoff = 4.5
prob_number_of_mag_sample_bins = 15
prob_number_of_events_in_zones = [5, 2, 10, 3, 3, 7]
prob_dip_in_zones = [35, 35, 35, 35, 35, 35]

# Attenuation
atten_models = ['Toro_1997_midcontinent']
atten_model_weights = [1]
atten_aggregate_Sa_of_atten_models = True
atten_use_variability = True
atten_variability_method = 2
atten_periods = [0.0, 0.30303000000000002, 1.0]
atten_threshold_distance = 400
atten_use_rescale_curve_from_pga = False
atten_override_RSA_shape = None
atten_cutoff_max_spectral_displacement = False
atten_pga_scaling_cutoff = 2
atten_smooth_spectral_acceleration = None
atten_log_sigma_eq_weight = 0

# Amplification
use_amplification = True
amp_use_variability = True
amp_variability_method = 2
amp_min_factor = 0.6
amp_max_factor = 10000

# Buildings
buildings_usage_classification = None
buildings_set_damping_Be_to_5_percent = None

# Capacity Spectrum Method
csm_use_variability = None
csm_variability_method = None
csm_standard_deviation = None
csm_damping_regimes = None
csm_damping_modify_Tav = True
csm_damping_use_smoothing = True
csm_use_hysteretic_damping = True
csm_hysteretic_damping = None
csm_SDcr_tolerance_percentage = None
csm_damping_max_iterations = None

# Loss
loss_min_pga = None
loss_regional_cost_index_multiplier = None
loss_aus_contents = None

# Save
save_hazard_map = True
save_total_financial_loss = False
save_building_loss = False
save_contents_loss = False
save_motion = False
save_prob_structural_damage = None

# General
site_tag = "newc" 
return_periods = [10, 50, 100, 200, 250, 474.56, 500, 974.78999999999996, 1000, 2474.9000000000001, 2500, 5000, 7500, 10000]
use_site_indexes = True
site_indexes = [
  2929 , 2655 , 946 , 5273 , 4990 , 4301 , 3432 , 4434 , 847 , 5241 , 
  1093 , 3191 , 1996 , 6129 , 2859 , 1974 , 837 , 1128 , 1212 , 4605 , 
  3162 , 5490 , 6155 , 3034 , 6028 , 4723 , 1357 , 1472 , 6024 , 3144 , 
  1555 , 2754 , 3443 , 2012 , 3711 , 6313 , 4794 , 5037 , 5368 , 5531 , 
  5868 , 4740 , 2002 , 3307 , 5082 , 4499 , 4994 , 3641 , 1851 , 789 , 
  4403 , 726 , 4386 , 808 , 3850 , 6087 , 2575 , 5515 , 1684 , 3817 , 
  3817 , 6047 , 1178 , 5727 , 3575 , 686 , 3734 , 5755 , 28 , 5263 , 
  1542 , 1239 , 5538 , 1493 , 2727 , 277 , 3550 , 3254 , 3606 , 5403 , 
  2337 , 5980 , 6276 , 2102 , 4877 , 2905 , 4003 , 476 , 6030 , 835 , 
  3363 , 455 , 525 , 5028 , 142 , 2455 , 1336 , 4741 , 4065 , 1102 , 
  3444 , 4013 , 6267 , 697 , 780 , 4939 , 209 , 4765 , 3538 , 2120 , 
  144 , 6075 , 639 , 4311 , 1791 , 2148 , 4950 , 1082 , 1645 , 3722 , 
  1791 , 1739 , 358 , 605 , 547 , 4397 , 2600 , 3840 , 4725 , 993 , 
  2929 , 5861 , 2201 , 2303 , 4886 , 5532 , 3014 , 2068 , 1919 , 1180 , 
  901 , 797 , 1184 , 273 , 602 , 3779 , 4287 , 466 , 1463 , 4970 , 
  5965 , 5225 , 4772 , 5308 , 4352 , 4540 , 4941 , 4880 , 5461 , 236 , 
  5439 , 2216 , 877 , 551 , 2821 , 2661 , 4308 , 1094 , 802 , 2875 , 
  125 , 2812 , 6211 , 4478 , 3143 , 6199 , 1881 , 1820 , 3600 , 1570 , 
  1071 , 6169 , 6337 , 4157 , 1866 , 67 , 2710 , 5686 , 4165 , 3508 , 
  1989 , 1441 , 2778 , 2742 , 247 , 1239 , 5143 , 5329 , 5153 , 49 , 
  1615 , 1233 , 2116 , 1240 , 2122 , 5529 , 1741 , 6319 , 198 , 5219 , 
  4947 , 3592 , 358 , 1264 , 6188 , 3230 , 1013 , 5164 , 2183 , 5170 , 
  1858 , 709 , 4700 , 3271 , 1456 , 1847 , 3609 , 468 , 4338 , 3558 , 
  442 , 3326 , 230 , 2909 , 1568 , 1448 , 4922 , 2382 , 3778 , 749 , 
  2536 , 3090 , 5937 , 964 , 4921 , 1537 , 5463 , 3257 , 6229 , 4126 , 
  409 , 1535 , 3996 , 4958 , 6114 , 2902 , 3416 , 5426 , 246 , 5854 , 
  4262 , 4572 , 4951 , 1110 , 4342 , 4075 , 2960 , 3550 , 4215 , 5265 , 
  1044 , 2640 , 522 , 5294 , 5405 , 1265 , 4483 , 797 , 1622 , 909 , 
  590 , 4713 , 6231 , 5566 , 6295 , 2491 , 5412 , 2648 , 2829 , 5045 , 
  5270 , 3301 , 3194 , 3702 , 1142 , 550 , 2264 , 5401 , 4690 , 2983 , 
  378 , 79 , 2383 , 4759 , 3648 , 2702 , 735 , 245 , 919 , 2002 , 
  4880 , 2734 , 4839 , 5346 , 4457 , 3648 , 4107 , 340 , 4755 , 1995 , 
  3177 , 5795 , 151 , 3275 , 3670 , 493 , 35 , 6092 , 4381 , 2748 , 
  2009 , 673 , 4051 , 3009 , 511 , 3787 , 3017 , 5607 , 2951 , 3127 , 
  6298 , 3291 , 3335 , 2769 , 1556 , 3418 , 2412 , 2653 , 5953 , 1854 , 
  1222 , 2219 , 4086 , 2661 , 3601 , 1801 , 6251 , 2360 , 5108 , 5052 , 
  446 , 1872 , 320 , 1887 , 3045 , 5933 , 3804 , 921 , 4812 , 1698 , 
  3245 , 4242 , 3172 , 3626 , 1340 , 5039 , 4448 , 1923 , 6142 , 2373 , 
  3022 , 1879 , 5702 , 5739 , 5215 , 1273 , 2098 , 2907 , 1964 , 5281 , 
  2828 , 189 , 4830 , 3453 , 2878 , 3522 , 1146 , 1302 , 5239 , 3179 , 
  3684 , 1971 , 3219 , 6218 , 6094 , 6143 , 4182 , 3650 , 3539 , 1253 , 
  6261 , 2289 , 6028 , 4017 , 3828 , 1421 , 3630 , 1003 , 3921 , 271 , 
  5748 , 3690 , 2815 , 3593 , 512 , 3374 , 5366 , 3786 , 806 , 6297 , 
  3241 , 3691 , 2685 , 2394 , 2739 , 4702 , 1237 , 4869 , 2565 , 1461 , 
  764 , 3121 , 4577 , 6318 , 6166 , 3329 , 17 , 4739 , 5891 , 257 , 
  2520 , 2360 , 1564 , 5576 , 3502 , 3967 , 4577 , 2418 , 5334 , 2789 , 
  4074 , 6097 , 6059 , 1358 , 2956 , 5015 , 6196 , 302 , 2939 , 2547 , 
  1275 , 1158 , 1561 , 1248 , 1458 , 5922 , 2274 , 275 , 4493 , 3394 , 
  3139 , 4844 , 1726 , 967 , 724 , 1558 , 3228 , 2618 , 5007 , 3676 , 
  2818 , 1411 , 4914 , 3259 , 3585 , 5557 , 3215 , 187 , 5358 , 410 , 
  746 , 2499 , 220 , 4142 , 2512 , 2914 , 3394 , 2398 , 4823 , 1273 , 
  3657 , 5143 , 3944 , 405 , 124 , 2737 , 6170 , 916 , 4824 , 685 , 
  1719 , 5077 , 441 , 6281 , 2351 , 1308 , 511 , 180 , 1338 , 587 , 
  1384 , 5659 , 1286 , 4541 , 4233 , 1176 , 1587 , 5064 , 743 , 584 , 
  5574 , 4983 , 2734 , 3850 , 3633 , 2 , 5106 , 1280 , 4002 , 569 , 
  5908 , 4207 , 214 , 1127 , 5023 , 373 , 573 , 3774 , 3618 , 4294 , 
  104 , 1195 , 6 , 3008 , 3940 , 4896 , 5312 , 617 , 445 , 5518 , 
  1432 , 4891 , 5293 , 5788 , 2946 , 124 , 1093 , 5218 , 4641 , 3592 , 
  5238 , 4810 , 1534 , 2917 , 3879 , 1530 , 5651 , 1718 , 3395 , 1394 , 
  5946 , 1960 , 2294 , 5771 , 1068 , 4330 , 1656 , 760 , 4023 , 3662 , 
  2191 , 6301 , 5252 , 1135 , 5905 , 5452 , 5634 , 3604 , 5940 , 2385 , 
  180 , 5235 , 3748 , 1899 , 2024 , 5816 , 5025 , 3863 , 4312 , 5947 , 
  4655 , 6227 , 3891 , 2888 , 4239 , 5007 , 2897 , 4570 , 5508 , 5568 , 
  1907 , 1029 , 3135 , 213 , 3993 , 5744 , 2053 , 3565 , 2973 , 1592 , 
  4130 , 909 , 1044 , 3504 , 1464 , 1262 , 664 , 854 , 4524 , 4039 , 
  1129 , 164 , 5427 , 2488 , 5674 , 1575 , 1445 , 5265 , 2137 , 1558 , 
  2102 , 5821 , 1539 , 1704 , 164 , 4312 , 3282 , 5856 , 3490 , 5406 , 
  2723 , 2003 , 198 , 4658 , 2134 , 3931 , 6111 , 3343 , 448 , 5541 , 
  1939 , 5551 , 3342 , 4149 , 4349 , 4202 , 5788 , 4635 , 3601 , 3166 , 
  5369 , 3821 , 1385 , 5001 , 1471 , 4894 , 642 , 568 , 5054 , 5794 , 
  5280 , 5332 , 4424 , 2460 , 494 , 3806 , 2832 , 1580 , 1255 , 2409 , 
  1909 , 823 , 1243 , 4672 , 4655 , 4518 , 2837 , 3515 , 4581 , 4433 , 
  3573 , 5774 , 2121 , 2039 , 5435 , 4755 , 3977 , 4424 , 3805 , 2563 , 
  3677 , 5874 , 665 , 4288 , 5142 , 1363 , 2512 , 5770 , 442 , 1113 , 
  125 , 2799 , 1278 , 3452 , 4413 , 4109 , 6049 , 5107 , 4016 , 6099 , 
  3263 , 1907 , 4730 , 5195 , 400 , 5327 , 1473 , 5510 , 1180 , 4602 , 
  5494 , 6031 , 3900 , 5299 , 1432 , 38 , 6299 , 5885 , 2688 , 1835 , 
  1016 , 4794 , 4283 , 372 , 1482 , 2302 , 2988 , 3416 , 5694 , 2579 , 
  421 , 4811 , 1636 , 939 , 1238 , 3777 , 2069 , 6045 , 2191 , 4473 , 
  5616 , 5071 , 2365 , 1535 , 2096 , 1709 , 1408 , 1904 , 4167 , 2461 , 
  5274 , 922 , 91 , 3568 , 3324 , 3726 , 5627 , 5890 , 3312 , 4617 , 
  1849 , 1754 , 2404 , 914 , 1119 , 3621 , 263 , 3461 , 1254 , 4406 , 
  6154 , 5327 , 5020 , 1685 , 3561 , 3228 , 1821 , 3144 , 4677 , 562 , 
  5054 , 5727 , 5350 , 6061 , 234 , 4854 , 5592 , 595 , 2404 , 3370 , 
  2364 , 802 , 4 , 3527 , 873 , 982 , 4004 , 3005 , 2531 , 5896 , 
  141 , 5125 , 2454 , 4334 , 883 , 2468 , 3332 , 2628 , 4818 , 5014 , 
  289 , 6106 , 3588 , 716 , 4225 , 1409 , 2788 , 1506 , 5735 , 5887 , 
  3779 , 6114 , 335 , 2483 , 6179 , 2027 , 3409 , 2005 , 3665 , 2554 , 
  5003 , 5008 , 624 , 584 , 1171 , 5974 , 5085 , 5435 , 4282 , 2744 , 
  3653 , 3746 , 5643 , 3845 , 249 , 5087 , 4917 , 5004 , 5361 , 3649 , 
  3007 , 2525 , 181 , 6304 , 5550 , 3628 , 5543 , 1677 , 73 , 6067 , 
  3720 , 2177 , 2056 , 3399 , 241 , 8 , 5634 , 1874 , 60 , 732 , 
  3079 , 2705 , 3876 , 4286 , 1673 , 2040 , 2819 , 1469 , 2497 , 3699 , 
  5188 , 892 , 5056 , 6182 , 1453 , 3504 , 4712 , 4339 , 1044 , 1873 , 
  419 , 4729 , 2803 , 2534 , 1053 , 1979 , 1051 , 841 , 1462 , 3809 , 
  4297 , 4458 , 4735 , 309 , 2232 , 939 , 3995 , 4476 , 305 , 3154 , 
  2020 , 2175 , 2671 , 5976 , 1346 , 2765 , 5092 , 3737 , 5075 , 3440 , 
  907 , 2403 , 3442 , 1525 , 2908 , 2053 , 429 , 1285 , 2478 , 5729 , 
  611 , 1558 , 5748 , 5993 , 1113 , 4539 , 900 , 5050 , 774 , 310 , 
  1664 , 2605 , 3266 , 4756 , 2195 , 2570 , 3983 , 3582 , 5221 , 3171 , 
  198 , 4345 , 45 , 3431 , 4953 , 5627 , 331 , 3682 , 6265 , 2338 , 
  575 , 5104 , 2761 , 3166 , 5666 , 840 , 3474 , 2480 , 834 , 4678 , 
  641 , 1982 , 468 , 6191 , 6193 , 1432 , 5841 , 1533 , 5568 , 897 , 
  3632 , 2601 , 2929 , 295 , 2734 , 3897 , 4221 , 6201 , 955 , 3286 , 
  2637 , 636 , 5951 , 2291 , 47 , 5432 , 878 , 2019 , 21 , 2257 , 
  3962 , 5466 , 4046 , 225 , 5366 , 3004 , 2362 , 116 , 2802 , 1327 , 
  6190 , 20 , 1472 , 6128 , 3075 , 1707 , 5141 , 391 , 2696 , 3229 , 
  1096 , 4080 , 6169 , 1217 , 2133 , 4721 , 2763 , 3334 , 6223 , 2767 , 
  439 , 4138 , 3135 , 555 , 1187 , 1168 , 902 , 5885 , 2296 , 5608 , 
  2620 , 3394 , 774 , 5052 , 1207 , 2193 , 5635 , 2394 , 5184 , 3211 , 
  4969 , 5840 , 2221 , 3924 , 569 , 3206 , 1945 , 2510 , 5231 , 3763 , 
  3060 , 4944 , 5304 , 5458 , 2744 , 858 , 1267 , 1378 , 1219 , 2598 , 
  254 , 4206 , 3468 , 2429 , 1665 , 2890 , 3183 , 3386 , 4960 , 4635 , 
  1682 , 5683 , 1034 , 4790 , 4845 , 6297 , 4477 , 3375 , 4808 , 5191 , 
  4552 , 2965 , 1795 , 2079 , 6255 , 226 , 4713 , 2157 , 588 , 3229 , 
  698 , 912 , 2974 , 5317 , 183 , 5421 , 2248 , 3847 , 5912 , 3831 , 
  383 , 1192 , 2343 , 2572 , 860 , 3604 , 2862 , 3382 , 1191 , 4548 , 
  116 , 2858 , 3799 , 2912 , 3016 , 500 , 1403 , 2505 , 5467 , 539 , 
  3864 , 5039 , 2547 , 1933 , 4539 , 595 , 3499 , 2088 , 5319 , 1999 , 
  5895 , 530 , 130 , 1997 , 1299 , 5798 , 3651 , 3275 , 1902 , 976 , 
  4186 , 6314 , 2654 , 2393 , 4092 , 3253 , 1748 , 4197 , 4651 , 1645 , 
  6313 , 5099 , 4445 , 1101 , 1620 , 2663 , 2133 , 3714 , 4166 , 4909 , 
  3321 , 3269 , 1527 , 5184 , 741 , 2823 , 755 , 3112 , 3940 , 4733 , 
  537 , 1501 , 876 , 2022 , 5226 , 1230 , 1634 , 4793 , 948 , 1764 , 
  241 , 5629 , 1782 , 5616 , 5195 , 5250 , 5309 , 5840 , 2907 , 5744 , 
  4593 , 5828 , 6058 , 1917 , 3128 , 1327 , 2027 , 828 , 3954 , 253 , 
  3230 , 1623 , 5782 , 2241 , 4658 , 4443 , 5213 , 70 , 3394 , 2508 , 
  4467 , 6130 , 1650 , 5111 , 60 , 4114 , 4472 , 1920 , 1981 , 1055 , 
  3466 , 2003 , 4995 , 2355 , 4250 , 4761 , 1576 , 4115 , 4403 , 972 , 
  918 , 1679 , 2393 , 4785 , 152 , 1016 , 2092 , 2459 , 5728 , 2213 , 
  5502 , 1166 , 708 , 5436 , 3875 , 477 , 2242 , 5851 , 4835 , 4530 , 
  1549 , 1291 , 2327 , 4668 , 958 , 1010 , 2258 , 2357 , 4534 , 1928 , 
  3007 , 5049 , 4344 , 3640 , 2345 , 826 , 2085 , 3658 , 943 , 909 , 
  5096 , 1597 , 968 , 2235 , 5063 , 1044 , 3297 , 5886 , 4037 , 913 , 
  2832 , 4309 , 3368 , 5906 , 461 , 3541 , 414 , 765 , 6070 , 3411 , 
  3306 , 4362 , 443 , 4900 , 2802 , 2726 , 1296 , 4894 , 3858 , 1819 , 
  6173 , 5672 , 5646 , 5020 , 2949 , 490 , 5388 , 4337 , 972 , 1860 , 
  5094 , 2817 , 6046 , 4707 , 6134 , 6054 , 2246 , 608 , 442 , 1848 , 
  6321 , 4525 , 2137 , 4908 , 13 , 4793 , 1080 , 4431 , 4264 , 555 , 
  521 , 1329 , 5427 , 162 , 4585 , 5105 , 2649 , 4032 , 3039 , 555 , 
  661 , 5675 , 3016 , 2859 , 3574 , 4613 , 5228 , 3141 , 2116 , 1567 , 
  2818 , 3679 , 2375 , 1422 , 4670 , 5518 , 4192 , 319 , 4693 , 4776 , 
  2567 , 3879 , 5089 , 1923 , 6104 , 5452 , 5863 , 1061 , 1211 , 3454 , 
  2097 , 2100 , 4159 , 2709 , 3083 , 4802 , 3168 , 6259 , 1884 , 1768 , 
  5998 , 382 , 3276 , 2332 , 1875 , 5370 , 856 , 4068 , 4055 , 4009 , 
  1078 , 3812 , 2348 , 668 , 1207 , 3660 , 3109 , 2194 , 6164 , 1466 , 
  1942 , 4 , 2716 , 1060 , 1669 , 5612 , 611 , 2316 , 599 , 5040 , 
  4998 , 1572 , 148 , 4201 , 2004 , 102 , 5985 , 237 , 2470 , 5416 , 
  4371 , 3736 , 2129 , 1434 , 1474 , 2000 , 1273 , 2873 , 1431 , 2491 , 
  4601 , 444 , 2219 , 750 , 4016 , 5408 , 4349 , 4836 , 3861 , 3918 , 
  5979 , 386 , 1035 , 1553 , 5747 , 852 , 6266 , 2941 , 5855 , 395 , 
  5687 , 1161 , 3219 , 2997 , 1171 , 6017 , 672 , 1029 , 4357 , 4792 , 
  3882 , 1013 , 2235 , 3830 , 6216 , 4810 , 1160 , 451 , 5016 , 1784 , 
  4362 , 62 , 3096 , 1171 , 5931 , 2715 , 2513 , 1455 , 5973 , 5690 , 
  921 , 3612 , 4068 , 4596 , 2014 , 1653 , 544 , 3736 , 3435 , 4589 , 
  418 , 4216 , 4415 , 3033 , 2976 , 3130 , 6256 , 741 , 4697 , 573 , 
  1154 , 2056 , 2712 , 2157 , 5598 , 3707 , 2759 , 4069 , 1662 , 1105 , 
  1935 , 383 , 2080 , 5433 , 3555 , 6044 , 567 , 4213 , 3527 , 3339 , 
  374 , 4426 , 4291 , 983 , 625 , 4096 , 5803 , 3036 , 1825 , 1407 , 
  117 , 5247 , 6090 , 6047 , 4202 , 6326 , 5213 , 428 , 116 , 2634 , 
  3914 , 2715 , 4179 , 1860 , 1611 , 2043 , 4488 , 1824 , 1003 , 6297 , 
  3240 , 444 , 3816 , 2187 , 674 , 5062 , 4148 , 5078 , 3608 , 5085 , 
  1095 , 1378 , 4120 , 4373 , 5925 , 6309 , 622 , 5892 , 4684 , 4754 , 
  5631 , 3970 , 5477 , 1915 , 4219 , 2031 , 5856 , 3817 , 709 , 5928 , 
  1763 , 6203 , 5264 , 1589 , 135 , 4699 , 3881 , 1517 , 5812 , 3960 , 
  2599 , 4782 , 4434 , 2421 , 795 , 4648 , 261 , 4238 , 4996 , 4669 , 
  5974 , 8 , 4848 , 299 , 4513 , 4185 , 4205 , 2093 , 2787 , 2949 , 
  1165 , 298 , 1355 , 3943 , 5488 , 1421 , 4471 , 4977 , 3011 , 1221 , 
  6305 , 441 , 659 , 578 , 5418 , 901 , 1959 , 500 , 2486 , 2977 , 
  188 , 2641 , 708 , 2134 , 3391 , 3147 , 6267 , 4085 , 4861 , 773 , 
  710 , 45 , 1943 , 2302 , 5816 , 5812 , 778 , 5834 , 2204 , 655 , 
  2063 , 3234 , 2537 , 5273 , 1151 , 4919 , 5184 , 700 , 5549 , 25 , 
  3499 , 4228 , 5634 , 1240 , 1252 , 3984 , 4303 , 4048 , 758 , 1240 , 
  673 , 5211 , 3271 , 1416 , 66 , 5959 , 4235 , 3169 , 1892 , 602 , 
  2027 , 1196 , 3841 , 2004 , 1813 , 911 , 5515 , 5271 , 2763 , 6308 , 
  5779 , 5970 , 117 , 6226 , 3415 , 5566 , 2573 , 1638 , 3232 , 4908 , 
  4349 , 4623 , 1658 , 2552 , 5732 , 2105 , 991 , 2799 , 1080 , 4856 , 
  6005 , 4044 , 1909 , 4624 , 4880 , 969 , 5297 , 4827 , 3574 , 498 , 
  1741 , 4226 , 2186 , 4217 , 5105 , 944 , 5351 , 2535 , 3030 , 2314 , 
  2376 , 689 , 4089 , 2766 , 4316 , 2761 , 2303 , 2816 , 6047 , 6201 , 
  5217 , 397 , 4398 , 1901 , 4035 , 876 , 3262 , 1177 , 2097 , 1430 , 
  4056 , 6260 , 1216 , 1 , 5138 , 5963 , 3051 , 2436 , 100 , 1470 , 
  5842 , 2040 , 4755 , 2005 , 829 , 983 , 362 , 3194 , 2964 , 3117 , 
  5275 , 6262 , 2922 , 2410 , 1960 , 5773 , 5575 , 919 , 922 , 2091 , 
  454 , 565 , 2396 , 3384 , 1507 , 4610 , 4210 , 1080 , 2450 , 472 , 
  910 , 3091 , 2150 , 5335 , 225 , 4153 , 6263 , 3903 , 3543 , 5087 , 
  1172 , 3706 , 1560 , 2489 , 2068 , 59 , 2122 , 4414 , 5635 , 2756 , 
  2036 , 529 , 1176 , 2461 , 2222 , 4126 , 2929 , 6143 , 3059 , 4793 , 
  270 , 2831 , 4293 , 2048 , 1208 , 2746 , 5461 , 5341 , 5534 , 5939 , 
  6180 , 144 , 180 , 286 , 2896 , 4639 , 1544 , 2588 , 1458 , 3309 , 
  4702 , 61 , 1734 , 2917 , 1502 , 5815 , 5090 , 3826 , 3974 , 1820 , 
  3760 , 5254 , 814 , 1512 , 5119 , 2708 , 3873 , 545 , 2080 , 4828 , 
  4035 , 1115 , 4740 , 4068 , 4686 , 4836 , 5676 , 3785 , 4909 , 450 , 
  5487 , 373 , 2069 , 6278 , 1789 , 5927 , 4980 , 1515 , 5311 , 1200 , 
  1088 , 4486 , 529 , 5547 , 4411 , 2921 , 3750 , 5755 , 3072 , 3122 , 
  4965 , 907 , 5607 , 2894 , 2744 , 6277 , 2057 , 3071 , 119 , 3125 , 
  681 , 535 , 4557 , 2470 , 3523 , 5585 , 6122 , 4094 , 1998 , 5207 , 
  4773 , 2129 , 5623 , 5064 , 4839 , 6173 , 1917 , 3946 , 5696 , 586 , 
  1968 , 779 , 5799 , 3301 , 3826 , 1271 , 4088 , 5565 , 2922 , 2784 , 
  2781 , 2060 , 905 , 913 , 2748 , 5472 , 4758 , 1777 , 5031 , 2191 , 
  2518 , 1041 , 1596 , 5729 , 472 , 3692 , 4950 , 1631 , 2402 , 3029 , 
  1518 , 5473 , 4902 , 5775 , 3984 , 3974 , 1308 , 3703 , 86 , 778 , 
  3439 , 5392 , 1268 , 3763 , 3994 , 2641 , 3507 , 909 , 3900 , 4208 , 
  3490 , 5755 , 736 , 2631 , 5214 , 2030 , 2093 , 2490 , 1804 , 3977 , 
  4770 , 4501 , 4055 , 4912 , 4365 , 331 , 2817 , 6329 , 1061 , 6193 , 
  1139 , 2244 , 1116 , 1491 , 2060 , 5701 , 876 , 6014 , 5816 , 2417 , 
  5205 , 4587 , 396 , 1473 , 5113 , 2821 , 2001 , 1133 , 5400 , 84 , 
  5756 , 3777 , 2889 , 1299 , 3999 , 3161 , 761 , 754 , 3271 , 2596 , 
  1055 , 5544 , 1856 , 844 , 5899 , 2383 , 4109 , 5363 , 6080 , 3737 , 
  952 , 1316 , 2514 , 2546 , 4581 , 2181 , 4014 , 3679 , 243 , 4512 , 
  2190 , 420 , 1073 , 3099 , 430 , 5041 , 6051 , 6167 , 5721 , 6149 , 
  3662 , 5531 , 5611 , 3052 , 2033 , 1438 , 1022 , 6181 , 2770 , 828 , 
  1661 , 4636 , 2129 , 4427 , 3946 , 2197 , 4210 , 3304 , 138 , 3859 , 
  4042 , 3887 , 3547 , 5743 , 5639 , 4752 , 2473 , 3264 , 3761 , 3214 , 
  269 , 4943 , 1546 , 803 , 2354 , 2780 , 4245 , 4420 , 3448 , 5442 , 
  6135 , 3467 , 1379 , 1207 , 245 , 3931 , 5110 , 20 , 3999 , 4218 , 
  5120 , 5791 , 4878 , 4488 , 4711 , 479 , 2336 , 2909 , 2076 , 5324 , 
  4777 , 1026 , 4042 , 5297 , 3756 , 3801 , 3155 , 3309 , 1557 , 2105 , 
  6144 , 660 , 2978 , 2792 , 4833 , 5744 , 3836 , 4293 , 1396 , 1226 , 
  3206 , 120 , 4754 , 2651 , 219 , 2792 , 6184 , 2326 , 4525 , 5174 , 
  66 , 3022 , 5010 , 3357 , 223 , 2922 , 3826 , 6026 , 1615 , 5679 , 
  4619 , 108 , 5080 , 2666 , 1837 , 2488 , 2068 , 4727 , 4045 , 6206 , 
  1213 , 275 , 3194 , 931 , 4031 , 6199 , 5323 , 4125 , 3713 , 5829 , 
  5077 , 225 , 1395 , 301 , 2477 , 4258 , 3768 , 5429 , 92 , 5358 , 
  5217 , 5483 , 244 , 4456 , 1184 , 3087 , 2866 , 4666 , 5276 , 1892 , 
  3321 , 3926 , 6138 , 3989 , 1794 , 5915 , 1588 , 1693 , 1189 , 2462 , 
  190 , 5265 , 3338 , 1188 , 3701 , 3733 , 3578 , 4921 , 2771 , 3777 , 
  712 , 4275 , 2089 , 2017 , 4212 , 2372 , 5092 , 2518 , 3722 , 1380 , 
  2039 , 3981 , 1297 , 4835 , 5627 , 3206 , 4621 , 1527 , 4881 , 4636 , 
  518 , 5150 , 5642 , 5098 , 2861 , 1507 , 3620 , 3663 , 1712 , 4840 , 
  2477 , 6089 , 6059 , 56 , 6083 , 5538 , 1933 , 1354 , 2499 , 5848 , 
  1700 , 6245 , 5433 , 3550 , 5872 , 4149 , 1335 , 2992 , 4660 , 3040 , 
  1679 , 323 , 785 , 3221 , 4062 , 3380 , 4160 , 3314 , 692 , 2191 , 
  1633 , 3746 , 5014 , 3244 , 2121 , 4229 , 4154 , 4673 , 4483 , 6004 , 
  1960 , 5258 , 1238 , 6236 , 4718 , 2653 , 3281 , 1974 , 1319 , 3146 , 
  3987 , 2309 , 3639 , 6326 , 4510 , 5529 , 3962 , 570 , 2039 , 5894 , 
  2768 , 1211 , 1666 , 802 , 5798 , 3715 , 1210 , 1398 , 1910 , 1100 , 
  4710 , 3019 , 927 , 3464 , 2771 , 6237 , 577 , 179 , 3805 , 893 , 
  2749 , 1677 , 5112 , 6106 , 4652 , 2780 , 1868 , 3231 , 3298 , 2407 , 
  298 , 2323 , 754 , 6196 , 2864 , 5382 , 3140 , 90 , 5717 , 2236 , 
  5637 , 130 , 5978 , 2955 , 2174 , 2265 , 3158 , 5929 , 1332 , 194 , 
  498 , 4988 , 25 , 2486 , 4897 , 4313 , 1280 , 3748 , 4641 , 5464 , 
  4523 , 3823 , 5373 , 1573 , 4524 , 1025 , 1589 , 3706 , 5737 , 2580 , 
  2022 , 3830 , 4128 , 4426 , 2715 , 5019 , 2773 , 4994 , 3204 , 264 , 
  3064 , 3858 , 4492 , 2201 , 4386 , 1913 , 705 , 5658 , 5594 , 576 , 
  5824 , 4570 , 1251 , 125 , 2658 , 4767 , 707 , 4485 , 4538 , 3854 , 
  293 , 3848 , 4154 , 3090 , 2536 , 5106 , 3458 , 5992 , 364 , 5057 , 
  4909 , 5773 , 100 , 2089 , 1241 , 4675 , 2266 , 5387 , 5969 , 579 , 
  2716 , 1654 , 4861 , 3842 , 4246 , 1035 , 6260 , 4201 , 6245 , 5119 , 
  3439 , 5494 , 810 , 593 , 6241 , 5916 , 3773 , 4397 , 4866 , 1143 , 
  2897 , 1286 , 1330 , 1365 , 2879 , 1363 , 713 , 4411 , 3131 , 719 , 
  1989 , 4589 , 5608 , 5955 , 1545 , 4586 , 5394 , 3528 , 4733 , 2088 , 
  4983 , 4028 , 5243 , 1862 , 4327 , 331 , 4774 , 2269 , 4102 , 2492 , 
  489 , 2707 , 2962 , 715 , 310 , 6091 , 977 , 1341 , 1155 , 3993 , 
  1790 , 4026 , 1409 , 744 , 3574 , 1916 , 5685 , 4346 , 5164 , 5177 , 
  4521 , 5612 , 3747 , 2981 , 1146 , 1740 , 4284 , 2181 , 1569 , 2759 , 
  5309 , 4286 , 2042 , 2535 , 4358 , 3982 , 1241 , 6299 , 3205 , 1124 , 
  4322 , 5498 , 3893 , 1258 , 5661 , 3055 , 1416 , 682 , 6167 , 2762 , 
  3736 , 4632 , 1111 , 6186 , 3484 , 4570 , 1413 , 1642 , 4075 , 614 , 
  1975 , 2983 , 3594 , 1615 , 5427 , 3352 , 6071 , 5992 , 2106 , 6282 , 
  3324 , 4798 , 4718 , 3150 , 5867 , 3823 , 1731 , 1371 , 2904 , 1083 , 
  5083 , 300 , 2807 , 1281 , 2545 , 4441 , 2173 , 3216 , 36 , 1499 , 
  2343 , 5799 , 1131 , 5849 , 4694 , 3702 , 4628 , 4758 , 1203 , 4965 , 
  4527 , 2149 , 5438 , 487 , 1020 , 4323 , 1882 , 5184 , 1923 , 291 , 
  4229 , 4155 , 4921 , 5215 , 4239 , 4738 , 499 , 2569 , 6004 , 4630 , 
  177 , 4645 , 1381 , 2567 , 1373 , 717 , 1390 , 957 , 4289 , 2678 , 
  798 , 602 , 5903 , 5723 , 4375 , 2871 , 1297 , 674 , 5212 , 1611 , 
  1792 , 1871 , 4261 , 5585 , 56 , 6207 , 2229 , 4686 , 554 , 1802 , 
  1658 , 3916 , 2266 , 135 , 2939 , 568 , 4227 , 726 , 3062 , 2250 , 
  2781 , 2767 , 4716 , 2168 , 2187 , 3955 , 5976 , 4827 , 3152 , 4622 , 
  3876 , 1468 , 3940 , 926 , 5449 , 3516 , 1047 , 351 , 1013 , 6094 , 
  4452 , 4728 , 133 , 5844 , 5593 , 2112 , 3106 , 6026 , 3305 , 397 , 
  1532 , 680 , 5972 , 4471 , 2568 , 1416 , 989 , 4903 , 6287 , 3604 , 
  6030 , 2588 , 5412 , 4418 , 1239 , 817 , 3643 , 4340 , 2189 , 199 , 
  5582 , 5128 , 1406 , 1446 , 2851 , 519 , 4969 , 151 , 3953 , 971 , 
  4015 , 722 , 1353 , 5390 , 3823 , 846 , 1938 , 4644 , 5903 , 5167 , 
  4862 , 5038 , 3096 , 2856 , 1034 , 6164 , 888 , 401 , 3201 , 3714 , 
  5734 , 4231 , 3477 , 1237 , 698 , 739 , 3993 , 1471 , 2970 , 440 , 
  4333 , 2913 , 89 , 2541 , 3429 , 1111 , 5698 , 6004 , 4046 , 3058 , 
  3678 , 2982 , 3229 , 1269 , 726 , 1503 , 5223 , 1354 , 4785 , 2531 , 
  1825 , 262 , 1671 , 5620 , 5527 , 4501 , 5517 , 5480 , 1285 , 6317 , 
  977 , 919 , 3949 , 2902 , 1171 , 2454 , 724 , 2023 , 6305 , 31 , 
  6020 , 4366 , 4126 , 5757 , 3607 , 4423 , 3215 , 2815 , 2119 , 2325 , 
  265 , 1409 , 4746 , 2235 , 5208 , 4046 , 4747 , 1843 , 3311 , 4014 , 
  3714 , 3015 , 6108 , 1975 , 579 , 4669 , 6131 , 2184 , 2346 , 2179 , 
  446 , 791 , 3897 , 2128 , 3187 , 4497 , 5366 , 5209 , 1805 , 4989 , 
  3017 , 5689 , 2318 , 2443 , 387 , 4652 , 2301 , 5122 , 4015 , 246 , 
  1839 , 2823 , 5663 , 4988 , 3566 , 4596 , 6078 , 2886 , 25 , 1716 , 
  4637 , 4431 , 6136 , 1370 , 3397 , 5239 , 4676 , 1159 , 2958 , 5023 , 
  1008 , 1309 , 3178 , 531 , 554 , 3159 , 5226 , 825 , 3380 , 1570 , 
  6234 , 1270 , 1277 , 3132 , 4439 , 4512 , 3037 , 5366 , 2051 , 3588 , 
  1488 , 5809 , 2513 , 2711 , 266 , 5538 , 675 , 4966 , 589 , 2156 , 
  54 , 4029 , 951 , 1140 , 1850 , 5023 , 6212 , 4420 , 3949 , 2718 , 
  805 , 1010 , 2337 , 5955 , 57 , 5628 , 4589 , 5847 , 5176 , 1866 , 
  293 , 213 , 3000 , 4837 , 4760 , 5461 , 4151 , 5113 , 3143 , 5869 , 
  5426 , 633 , 949 , 2016 , 3321 , 628 , 6201 , 3040 , 5034 , 98 , 
  3036 , 5684 , 2323 , 2532 , 2743 , 1756 , 2318 , 5089 , 548 , 4160 , 
  3021 , 1422 , 3424 , 4713 , 3130 , 3061 , 4579 , 3985 , 4471 , 5407 , 
  3262 , 3562 , 2285 , 5290 , 4419 , 3027 , 53 , 3869 , 4083 , 3178 , 
  2655 , 1444 , 5914 , 4027 , 3751 , 995 , 1202 , 1524 , 5781 , 4105 , 
  3211 , 4212 , 4649 , 2797 , 679 , 5441 , 2510 , 3769 , 766 , 5868 , 
  4152 , 4406 , 6298 , 3146 , 352 , 1241 , 855 , 1204 , 3999 , 4464 , 
  5528 , 6044 , 1535 , 5136 , 5523 , 5481 , 972 , 896 , 3983 , 3308 , 
  25 , 4934 , 3354 , 5270 , 5203 , 1247 , 697 , 3691 , 4994 , 1236 , 
  234 , 5387 , 2594 , 1150 , 1091 , 5666 , 502 , 293 , 3674 , 2756 , 
  2590 , 3587 , 6105 , 4271 , 4034 , 1110 , 257 , 2448 , 4839 , 6203 , 
  507 , 4578 , 5869 , 4398 , 1627 , 6321 , 6114 , 5999 , 4836 , 1044 , 
  5765 , 2245 , 1734 , 5230 , 1515 , 3474 , 230 , 646 , 2658 , 4818 , 
  3917 , 3877 , 1370 , 411 , 1189 , 3431 , 2601 , 2749 , 1008 , 1772 , 
  1057 , 1460 , 5116 , 903 , 3954 , 2578 , 1044 , 6284 , 4133 , 585 , 
  6118 , 3414 , 857 , 2192 , 3344 , 2540 , 201 , 972 , 2670 , 2078 , 
  1325 , 1830 , 2476 , 1675 , 3177 , 5109 , 1131 , 1305 , 2175 , 3205 , 
  2652 , 2207 , 1913 , 2402 , 1239 , 2012 , 4760 , 5631 , 3562 , 6313 , 
  1214 , 2652 , 6145 , 1972 , 5176 , 4890 , 1983 , 2868 , 3601 , 4643
  ]
site_db_tag = "" 
input_dir = r"..\implementation_tests\input/" 
output_dir = r".\benchmark_output\TS_haz08/" 

# If this file is executed the simulation will start.
# Delete all variables that are not EQRM parameters variables. 
if __name__ == '__main__':
    from eqrm_code.analysis import main
    main(locals())
