from scripts.work_meta_default import WorkMeta_default

class WorkMeta(WorkMeta_default):
    # заливка:
    # python $PWBPATH/pwb.py pagefromfile -file:'/tmp/topost.txt' -notitle -summary:"заливка" -pt:1 -dir:~/.pywikibot/ -family:wikisource -user:TextworkerBot -force

    # Настройки заливаемых сканов -------------------------------------

    # 'Ницше Так говорил Заратустра 1913.pdf'
    directory = '/home/vladislav/var/chin_fb2'
    filepaths_output_pwb = '/tmp/chinskiy.txt'
    workpagename = 'Чинский. Орден мартинистов.pdf'
    range_pages_metric = [
        [0, 0, 0, True],
    ]
    from_scanpagenum = 0  # делать страницы начиная с этой
    parse_from = 'fb2'  # 'fb2', 'htm', 'txt'
    wrap_to_VARtpl = True
    deyatification = True
    make_colontitul = dict(enable=False, on_top=True, center_only=False)
    do_precorrection = True
    to_NSpages = True

# class WorkMeta(WorkMeta_default):
#     # заливка:
#     # python $PWBPATH/pwb.py pagefromfile -file:'/tmp/topost.txt' -notitle -summary:"заливка" -pt:1 -dir:~/.pywikibot/ -family:wikisource -user:TextworkerBot -force
#
#     # Настройки заливаемых сканов -------------------------------------
#
#     # 'Ницше Так говорил Заратустра 1913.pdf'
#     directory = '/home/vladislav/var/chinskiy_fb2'
#     filepaths_output_pwb = '/tmp/chinskiy.txt'
#     workpagename = 'Процесс Чинского, 1908.pdf'
#     range_pages_metric = [
#         [0, 0, 0, True],
#     ]
#     from_scanpagenum = 0  # делать страницы начиная с этой
#     parse_from = 'fb2'  # 'fb2', 'htm', 'txt'
#     wrap_to_VARtpl = True
#     deyatification = True
#     make_colontitul = dict(enable=False, on_top=True, center_only=False)
#     do_precorrection = True
#     to_NSpages = True

# class WorkMeta(WorkMeta_default):
#     # заливка:
#     # python $PWBPATH/pwb.py pagefromfile -file:'/tmp/topost.txt' -notitle -summary:"заливка" -pt:1 -dir:~/.pywikibot/ -family:wikisource -user:TextworkerBot -force
#
#     # Настройки заливаемых сканов -------------------------------------
#     to_NSpages = False
#     input_csv = '/home/vladislav/workspace/scraping/tolstoy_ru/bean.csv'  # if to_NSpages
#     directory = None
#     # filepaths_output_pwb = '/tmp/kuzn.txt'
#     workpagename = 'Кузнецова В. Г. Материалы по праздникам и обрядам амгуэмских оленных чукчей.pdf'
#     range_pages_metric = [
#         [0, 0, 0, True],
#     ]
#     from_scanpagenum = 0  # делать страницы начиная с этой
#     parse_from = 'htm'  # 'fb2', 'htm', 'txt'
#     wrap_to_VARtpl = False
#     deyatification = False
#     make_colontitul = dict(enable=False, on_top=True, center_only=False)
#     do_precorrection = True
#     # do_perenos_words = True


# class WorkMeta(WorkMeta_default):
#     # заливка:
#     # python $PWBPATH/pwb.py pagefromfile -file:'/tmp/topost.txt' -notitle -summary:"заливка" -pt:1 -dir:~/.pywikibot/ -family:wikisource -user:TextworkerBot -force
#
#     # Настройки заливаемых сканов -------------------------------------
#
#     # 'Ницше Так говорил Заратустра 1913.pdf'
#     directory = '/home/vladislav/var/Кузнецова-fb2'
#     filepaths_output_pwb = '/tmp/kuzn.txt'
#     workpagename = 'Кузнецова В. Г. Материалы по праздникам и обрядам амгуэмских оленных чукчей.pdf'
#     range_pages_metric = [
#         [0, 0, 0, True],
#     ]
#     from_scanpagenum = 0  # делать страницы начиная с этой
#     parse_from = 'htm'  # 'fb2', 'htm', 'txt'
#     wrap_to_VARtpl = False
#     deyatification = False
#     make_colontitul = dict(enable=False, on_top=True, center_only=False)
#     do_precorrection = True


# class WorkMeta(Work_meta_default):
#     # заливка:
#     # python $PWBPATH/pwb.py pagefromfile -file:'/tmp/topost.txt' -notitle -summary:"заливка" -pt:1 -dir:~/.pywikibot/ -family:wikisource -user:TextworkerBot -force
#
#     # Настройки заливаемых сканов -------------------------------------
#
#     # 'Ницше Так говорил Заратустра 1913.pdf'
#     directory = '/home/vladislav/var/Кузнецова-fb2'
#     filepaths_output_pwb = '/tmp/kuzn.txt'
#     workpagename = 'Кузнецова В. Г. Материалы по праздникам и обрядам амгуэмских оленных чукчей.pdf'
#     range_pages_metric = [
#         [0, 0, 0, True],
#     ]
#     from_scanpagenum = 0  # делать страницы начиная с этой
#     parse_from = 'fb2'  # 'fb2', 'htm', 'txt'
#     wrap_to_VARtpl = False
#     deyatification = False
#     make_colontitul = dict(enable=False, on_top=True, center_only=False)
#     do_precorrection = True


# # 'Ницше Так говорил Заратустра 1913.pdf'
# directory = '/home/vladislav/var/nitsche-txt'
# filepaths_output_pwb = '/tmp/nitche.txt'
# workpagename = 'Ницше Так говорил Заратустра 1913.pdf'
# range_pages_metric = [
#     [0, 0, 0, True],
# ]
# from_scanpagenum = 0  # делать страницы начиная с этой
# parse_from = 'txt'  # 'fb2', 'htm', 'txt'
# wrap_to_VARtpl = True
# deyatification = True
# make_colontitul = dict(enable=False, on_top=True, center_only=True)
# do_precorrection = True


# # Евтидем (Платон, 1878).pdf
# m.directory = '/home/vladislav/var/sofist'
# m.filepaths_output_pwb = '/tmp/sofist.txt'
# m.workpagename = 'Софист (Платон, 1907).pdf'
# m.range_pages_metric = [
#     [-7, 8, 209, True],
# ]
# m.from_scanpagenum = 0  # делать страницы начиная с этой
# m.parse_from = 'htm'  # 'fb2', 'htm'
# m.wrap_to_VARtpl = True
# m.deyatification = True
# m.colontitul_on_top = True
# m.colontitul_center_only = True
# m.do_precorrection = True


# Евтидем (Платон, 1878).pdf
# m.directory = '/home/vladislav/var/evtidem'
# m.filepaths_output_pwb = '/tmp/evtidem.txt'
# m.workpagename = 'Евтидем (Платон, 1878).pdf'
# m.range_pages_metric = [
#     [0, 1, 5, None],
#     [-1, 6, 33, True],
#     [-5, 38, 136, True],
# ]
# m.from_scanpagenum = 0  # делать страницы начиная с этой
# m.parse_from = 'htm'  # 'fb2', 'htm'
# m.wrap_to_VARtpl = True
# m.deyatification = True
# m.colontitul_on_top = True
# m.colontitul_center_only = True
# m.do_precorrection = True
#

# Menon
# m.directory = '/home/vladislav/var/menon'
# m.filepaths_output_pwb = '/tmp/menon.txt'
# m.workpagename = 'Менон (Платон, 1868).pdf'
# m.range_pages_metric = [
#     [-1, 6, 21, False],
#     [-21, 22, 162, True],
# ]
# m.from_scanpagenum = 0  # делать страницы начиная с этой
# m.parse_from = 'htm'  # 'fb2', 'htm'
# m.wrap_to_VARtpl = True
# m.deyatification = True
# m.colontitul_on_top = True
# m.colontitul_center_only = True
# m.do_precorrection = True


class Meta_gegel1916_3:
    directory = '/home/vladislav/var/gegel1916-3-html'
    filepaths_output_pwb = '/tmp/gegel-1916-3.txt'
    workpagename = 'Гегель Г.В.Ф. - Наука логики. Т. 3 - 1916.djvu'
    range_pages_metric = [
        [-1, 1, 9, True],
        [-9, 10, 235, False],
    ]
    from_scanpagenum = 0  # делать страницы начиная с этой
    parse_from = 'htm'  # 'fb2', 'htm'
    wrap_to_VARtpl = True
    deyatification = True
    colontitul_on_top = True
    colontitul_center_only = True
    do_precorrection = True
    fext = f'.{parse_from}'


class Meta_gegel1916_2:
    directory = '/home/vladislav/var/gegel1916-2-html'
    filepaths_output_pwb = '/tmp/gegel-1916-2.txt'
    workpagename = 'Гегель Г.В.Ф. - Наука логики. Т. 2 - 1916.djvu'
    range_pages_metric = [
        [-1, 1, 9, True],
        [-9, 10, 167, False],
    ]
    from_scanpagenum = 0  # делать страницы начиная с этой
    parse_from = 'htm'  # 'fb2', 'htm'
    wrap_to_VARtpl = True
    deyatification = True
    colontitul_on_top = True
    colontitul_center_only = True
    do_precorrection = True
    fext = f'.{parse_from}'


class Meta_gegel1916_1:
    directory = '/home/vladislav/var/gegel1916-1-html'
    filepaths_output_pwb = '/tmp/gegel-1916-1.txt'
    workpagename = 'Гегель Г.В.Ф. - Наука логики. Т. 1 - 1916.djvu'
    range_pages_metric = [
        [-1, 1, 37, True],
        [-37, 38, 311, False],
    ]
    from_scanpagenum = 0  # делать страницы начиная с этой
    parse_from = 'htm'  # 'fb2', 'htm'
    wrap_to_VARtpl = True
    deyatification = True
    colontitul_on_top = True
    colontitul_center_only = True
    do_precorrection = True
    fext = f'.{parse_from}'


class Meta_gegel1913:
    directory = '/home/vladislav/var/gegel-fd-html'
    filepaths_output_pwb = '/tmp/gegel-fd.txt'
    workpagename = 'Гегель Г.В.Ф. - Феноменология духа - 1913.djvu'
    range_pages_metric = [
        [-1, 1, 37, True],
        [-37, 38, 415, False],
    ]
    from_scanpagenum = 4  # делать страницы начиная с этой
    parse_from = 'htm'  # 'fb2', 'htm'
    wrap_to_VARtpl = True
    deyatification = True
    colontitul_on_top = True
    colontitul_center_only = False
    do_precorrection = True
    fext = f'.{parse_from}'


class Meta_platon_feetit:
    directory = '/home/vladislav/var/platon-feetit-fb2'
    filepaths_output_pwb = '/tmp/feetit.txt'
    workpagename = 'Теэтет (Платон, Добиаш).pdf'
    range_pages_metric = [
        [-5, 7, 123, False],
    ]
    parse_from_fb2_file = True
    wrap_to_VARtpl = True
    deyatification = True
    colontitul_on_top = True
    colontitul_center_only = True
    do_precorrection = True


class Meta_platon_protagor:
    directory = '/home/vladislav/var/platon-protagor-fb2'
    filepaths_output_pwb = '/tmp/protagor.txt'
    workpagename = 'Протагор (Платон, Добиаш).pdf'
    range_pages_metric = [
        [-3, 7, 80, False],
    ]
    parse_from_fb2_file = True
    wrap_to_VARtpl = True
    deyatification = True
    colontitul_on_top = True
    colontitul_center_only = False
    do_precorrection = True


class Meta_platon_timeykritiy1883:
    directory = '/home/vladislav/var/platon-timeykritiy1883-fb2'
    filepaths_output_pwb = '/tmp/timeykritiy.txt'
    workpagename = 'Тимей и Критий (Платон, Малеванский).pdf'
    range_pages_metric = [
        [-5, 7, 243, False],
        [-243, 245, 279, False],
        [-279, 281, 307, False],
    ]
    parse_from_fb2_file = True
    wrap_to_VARtpl = True
    deyatification = True
    colontitul_on_top = True
    colontitul_center_only = True
    do_precorrection = True


class Meta_platon_zakoni:
    directory = '/home/vladislav/var/platon-zakoni-fb2'
    filepaths_output_pwb = '/tmp/zakoni.txt'
    workpagename = 'Платоновы разговоры о законах (Платон, Оболенский).pdf'
    range_pages_metric = [
        [-6, 7, 10, True],  # римские цифры
        [-10, 11, 565, False],
    ]
    parse_from_fb2_file = True
    wrap_to_VARtpl = True
    deyatification = True
    colontitul_on_top = True
    colontitul_center_only = True
    do_precorrection = True


class Meta_platon_fedon:
    directory = '/home/vladislav/var/platon-fedon-fb2'
    filepaths_output_pwb = '/tmp/fedon.txt'
    workpagename = 'Федон (Платон, Лебедев).pdf'
    range_pages_metric = [
        [-1, 7, 157, False],
    ]
    parse_from_fb2_file = True
    deyatification = True
    colontitul_center_only = True
    wrap_to_VARtpl = True
    do_precorrection = True


class Meta_platon_pir:
    slug = 'pir'
    # directory = f'/home/vladislav/var/platon-{slug}-fb2'
    directory = f'/home/vladislav/var/platon-{slug}-fb2-fr12'
    filepaths_output_pwb = f'/tmp/{slug}.txt'
    workpagename = 'Пир (Платон, Городецкий).pdf'
    range_pages_metric = [
        [-8, 9, 109, False],
    ]
    parse_from_fb2_file = True
    deyatification = True
    colontitul_center_only = False
    colontitul_on_top = False
    wrap_to_VARtpl = True
    do_precorrection = True

# meta_works = [
#     dict(
#         directory='/home/vladislav/var/platon-fedon-fb2',
#         filepaths_output_pwb='/tmp/fedon.txt',
#         workpagename='Федон (Платон, Лебедев).pdf',
#         range_pages_metric=[
#             [-1, 7, 157],
#         ],
#         deyatification=True,
#         parse_from_fb2_file=True,
#         colontitul_center_only=True,
#         wrap_to_VARtpl=True,
#         do_precorrection=True,
#     ),
#
#     dict(
#         slug='pir',
#         directory=f'/home/vladislav/var/platon-pir-fb2',
#         filepaths_output_pwb=f'/tmp/pir.txt',
#         workpagename='Пир (Платон, Городецкий).pdf',
#         range_pages_metric=[
#             [-1, 7, 157],
#         ],
#         deyatification=True,
#         parse_from_fb2_file=True,
#         colontitul_center_only=False,
#         colontitul_on_top=False,
#         wrap_to_VARtpl=True,
#         do_precorrection=True,
#     )
# ]
# m = Dict2class(meta_works[1])
