import sys
"""adding path to look for modules"""
sys.path.append(r"C:\AU-PHD\General_Data\_Python\modules")
from prf_plot_tools import prepare_refinement_result

def test_prepare_refinement_result_R1D1_1():
    phases = {'1': '$\\gamma$-Fe$_2$O$_3$', '2': 'Fe$_3$O$_4$'}
    refined_par = {'R wp / chi2': (10.8, 4.094), 'Cell_A_ph1_pat1': (8.357975, 0.00049791916),
        'Zero_pat1': (0.02134739, 0.0019006323), 'Bck_0_pat1': (294.35812, 0.93447328),
        'Cell_C_ph1_pat1': (8.320617, 0.000006885301), 'Cell_A_ph2_pat1': (8.3551588, 0.00022619251),
        'Scale_ph1_pat1': (0.0010213042, 1.4571761e-02), 'Bover_ph1_pat1': (1.8148999, 0.12363505),
        'Y-cos_ph1_pat1': (0.44642535, 0.0044327537), 'Scale_ph2_pat1': (0.00061019335, 1.313103e-05),
        'Bover_ph2_pat1': (1.1993476, 0.16561012), 'Y-cos_ph2_pat1': (0.34181476, 0.0056125615)}
    size_info = {'$\\gamma$-Fe$_2$O$_3$': {'ab-size': (14.629360729774538, 0.1452613587099003),
        'c-size': (14.629360729774538, 0.1452613587099003)},
        'Fe$_3$O$_4$': {'ab-size': (19.106598802421093, 30.3137282919977323),
        'c-size': (19.106598802421093, 30.3137282919977323)}}
    frac_info = {'$\\gamma$-Fe$_2$O$_3$': (65.23, 1.21), 'Fe$_3$O$_4$': (34.77, 0.86)}
    separation = ""
    spacegroups = {'1': 'P 43 21 2', '2': 'F d -3 m'}

    combined_text = prepare_refinement_result(phases, refined_par, size_info, frac_info, separation, spacegroups)
    answer = 'R wp / chi2      10.8 / 4.09\n'
    answer += 'Zero_pat1        0.021(2)      \n\n' # 'Zero_pat1': (0.02134739, 0.0019006323)
    answer += 'P 43 21 2        $\\gamma$-Fe$_2$O$_3$\n'
    answer += 'Bover_ph1_pat1   1.8(1)        \n' # 'Bover_ph1_pat1': (1.8148999, 0.12363505)
    answer += 'Scale_ph1_pat1   0.00(1)       \n' # 'Scale_ph1_pat1': (0.0010213042, 0.014571761)
    answer += 'Y-cos_ph1_pat1   0.446(4)      \n' # 'Y-cos_ph1_pat1': (0.44642535, 0.0044327537)
    answer += 'Cell_A_ph1_pat1  8.3580(5)     [$\\AA$]\n' # 'Cell_A_ph1_pat1': (8.357975, 0.00049791916)
    answer += 'Cell_C_ph1_pat1  8.320617(7)   [$\\AA$]\n' # 'Cell_C_ph1_pat1': (8.320617, 0.000006885301)
    answer += 'abc-size         14.6(1)       [nm]\n' # 'ab-size': (14.629360729774538, 0.1452613587099003)
    answer += 'phase fraction   65(1)         [%]\n\n' # '$\\gamma$-Fe$_2$O$_3$': (65.23, 1.21)
    answer += 'F d -3 m         Fe$_3$O$_4$\n'
    answer += 'Bover_ph2_pat1   1.2(2)        \n' # 'Bover_ph2_pat1': (1.1993476, 0.16561012)
    answer += 'Scale_ph2_pat1   0.00061(1)    \n' # 'Scale_ph2_pat1': (0.00061019335, 0.00001313103)
    answer += 'Y-cos_ph2_pat1   0.342(6)      \n' # 'Y-cos_ph2_pat1': (0.34181476, 0.0056125615)
    answer += 'Cell_A_ph2_pat1  8.3552(2)     [$\\AA$]\n' # 'Cell_A_ph2_pat1': (8.3551588, 0.00022619251)
    answer += 'abc-size         2(3)e+01      [nm]\n' # 'ab-size': (19.106598802421093, 30.3137282919977323)
    answer += 'phase fraction   34.8(9)       [%]\n\n' # 'Fe$_3$O$_4$': (34.77, 0.86)

    assert combined_text == answer
#
def test_prepare_refinement_result_R1D1_2():
    phases = {'1': '$\\gamma$-Fe$_2$O$_3$', '2': 'Fe$_3$O$_4$'}
    refined_par = {'R wp / chi2': (8.28, 2.012), 'Cell_A_ph1_pat1': (8.3699255, 0.00080950302),
        'Zero_pat1': (0.048056044, 0.003031668), 'Bck_0_pat1': (357.74515, 0.91857326),
        'Bck_1_pat1': (-202.75655, 1.2903143), 'Bck_2_pat1': (56.52343, 1.1799482),
        'Cell_C_ph1_pat1': (8.2970295, 0.00088596455), 'Cell_A_ph2_pat1': (8.3640728, 0.00050848734),
        'Bck_3_pat1': (-14.924565, 1.0265242), 'Bck_4_pat1': (-16.455841, 1.0073256),
        'Bck_5_pat1': (-14.50427, 0.96515596), 'Scale_ph1_pat1': (0.00045547288, 9.0843623e-06),
        'Bover_ph1_pat1': (-0.87831533, 0.031517573), 'Y-cos_ph1_pat1': (0.76573592, 0.0028212941),
        'Scale_ph2_pat1': (0.0011484402, 9.6892345e-06), 'Bck_6_pat1': (38.836193, 0.99057782),
        'Bck_7_pat1': (-33.730961, 0.85562229), 'Bck_8_pat1': (-4.4012966, 0.83337075)}
    size_info = {'$\\gamma$-Fe$_2$O$_3$': {'ab-size': (8.528942306984703, 0.031424220780887926),
        'c-size': (8.528942306984703, 0.031424220780887926)}}
    frac_info = {'$\\gamma$-Fe$_2$O$_3$': (30.71, 0.67), 'Fe$_3$O$_4$': (69.29, 0.83)}
    separation = ""
    spacegroups = {'1': 'P 43 21 2', '2': 'F d -3 m'}

    combined_text = prepare_refinement_result(phases, refined_par, size_info, frac_info, separation, spacegroups)
    answer = 'R wp / chi2      8.28 / 2.01\n'            #
    answer += 'Zero_pat1        0.048(3)      \n\n'        #
    answer += 'P 43 21 2        $\\gamma$-Fe$_2$O$_3$\n' #
    answer += 'Bover_ph1_pat1   -0.88(3)      \n'          # 'Bover_ph1_pat1': (-0.87831533, 0.031517573)
    answer += 'Scale_ph1_pat1   0.000455(9)   \n'          # 'Scale_ph1_pat1': (0.00045547288, 0.0000090843623)
    answer += 'Y-cos_ph1_pat1   0.766(3)      \n'          #
    answer += 'Cell_A_ph1_pat1  8.3699(8)     [$\\AA$]\n'  #
    answer += 'Cell_C_ph1_pat1  8.2970(9)     [$\\AA$]\n'  #
    answer += 'abc-size         8.53(3)       [nm]\n'      #
    answer += 'phase fraction   30.7(7)       [%]\n\n'     #
    answer += 'F d -3 m         Fe$_3$O$_4$\n'           #
    answer += 'Scale_ph2_pat1   0.00115(1)    \n'          # 'Scale_ph2_pat1': (0.0011484402, 0.0000096892345)
    answer += 'Cell_A_ph2_pat1  8.3641(5)     [$\\AA$]\n'  #
    answer += 'phase fraction   69.3(8)       [%]\n\n'     #

    assert combined_text == answer

def test_prepare_refinement_result_DMC():
    phases = {'1': 'Fe$_3$O$_4$ nuclear', '2': 'Fe$_3$O$_4$ magnetic', '3': '$\\alpha$-Fe nuclear', '4': 'FeO nuclear'}
    refined_par = {'R wp / chi2': (37.6, 19.81), 'Bck_0_pat1': (112.72535, 2.4259808),
        'Scale_ph1_pat1': (0.18022682, 0.0071173995), 'Cell_A_ph3_pat1': (2.8646729, 0.00045378957),
        'Scale_ph3_pat1': (62.647964, 1.6080902), 'Rx_FeTd_ph2': (-4.1363354, 0.13851264),
        'Cell_A_ph1_pat1': (8.385622, 0.0018837955), 'Y-cos_ph3_pat1': (0.027515559, 0.014522476),
        'Zero_pat1': (-0.04782128, 20.025845908), 'Y-cos_ph1_pat1': (0.2225723, 0.022096494),
        'Cell_A_ph4_pat1': (4.3009143, 0.0015226558), 'Scale_ph4_pat1': (1.2392763, 0.15119411),
        'Y-cos_ph4_pat1': (0.23840357, 0.0)}
    size_info = {'$\\alpha$-Fe nuclear': {'ab-size': (325.99387114562995, 172.05676867620622),
        'c-size': (325.99387114562995, 172.05676867620622)}, 'Fe$_3$O$_4$ nuclear': {'ab-size': (40.301077875126325, 4.001003383894859),
        'c-size': (40.301077875126325, 4.001003383894859)}, 'FeO nuclear': {'ab-size': (37.62487111726547, 8.995371307732798),
        'c-size': (37.62487111726547, 8.995371307732798)}}
    frac_info = {'Fe$_3$O$_4$ nuclear': (45.5, 2.1), '$\\alpha$-Fe nuclear': (46.49, 1.62), 'FeO nuclear': (8.01, 1.0)}
    separation = ""
    spacegroups = {'1': 'F d -3 m', '2': 'F -1', '3': 'I m -3 m', '4': 'F m -3 m'}

    combined_text = prepare_refinement_result(phases, refined_par, size_info, frac_info, separation, spacegroups)
    answer = 'R wp / chi2      37.6 / 19.8\n'            # 'R wp / chi2': (37.6, 19.81)
    answer += 'Zero_pat1        -0(2)e+01     \n\n'        # 'Zero_pat1': (-0.04782128, 20.025845908)
    answer += 'I m -3 m         $\\alpha$-Fe nuclear\n'  #
    answer += 'Scale_ph3_pat1   63(2)         \n'          # 'Scale_ph3_pat1': (62.647964, 1.6080902)
    answer += 'Y-cos_ph3_pat1   0.03(1)       \n'          # 'Y-cos_ph3_pat1': (0.027515559, 0.014522476)
    answer += 'Cell_A_ph3_pat1  2.8647(5)     [$\\AA$]\n'  # 'Cell_A_ph3_pat1': (2.8646729, 0.00045378957)
    answer += 'abc-size         3(2)e+02      [nm]\n'      # 'ab-size': (325.99387114562995, 172.05676867620622)
    answer += 'phase fraction   46(2)         [%]\n\n'     # '$\\alpha$-Fe nuclear': (46.49, 1.62)
    answer += 'F -1             Fe$_3$O$_4$ magnetic\n'  #
    answer += 'Rx_FeTd_ph2      -4.1(1)       \n\n'        # 'Rx_FeTd_ph2': (-4.1363354, 0.13851264)
    answer += 'F d -3 m         Fe$_3$O$_4$ nuclear\n'   #
    answer += 'Scale_ph1_pat1   0.180(7)      \n'          # 'Scale_ph1_pat1': (0.18022682, 0.0071173995)
    answer += 'Y-cos_ph1_pat1   0.22(2)       \n'          # 'Y-cos_ph1_pat1': (0.2225723, 0.022096494)
    answer += 'Cell_A_ph1_pat1  8.386(2)      [$\\AA$]\n'  #
    answer += 'abc-size         40(4)         [nm]\n'      # 'ab-size': (40.301077875126325, 4.001003383894859)
    answer += 'phase fraction   46(2)         [%]\n\n'     # 'Fe$_3$O$_4$ nuclear': (45.5, 2.1)
    answer += 'F m -3 m         FeO nuclear\n'           #
    answer += 'Scale_ph4_pat1   1.2(2)        \n'          # 'Scale_ph4_pat1': (1.2392763, 0.15119411)
    answer += 'Y-cos_ph4_pat1   0.23840357(0) \n'          # 'Y-cos_ph4_pat1': (0.23840357, 0.0)
    answer += 'Cell_A_ph4_pat1  4.301(2)      [$\\AA$]\n'  # 'Cell_A_ph4_pat1': (4.3009143, 0.0015226558)
    answer += 'abc-size         38(9)         [nm]\n'      # 'ab-size': (37.62487111726547, 8.995371307732798)
    answer += 'phase fraction   8(1)          [%]\n\n'     # 'FeO nuclear': (8.01, 1.0)

    assert combined_text == answer
#
