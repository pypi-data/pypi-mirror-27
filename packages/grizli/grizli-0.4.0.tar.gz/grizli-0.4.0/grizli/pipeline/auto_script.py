"""
Automatic processing scripts for grizli
"""
        
# Only fetch F814W optical data for now
ONLY_F814W = True

def demo():
    """
    Test full pipeline, program #12471
    """
    
    import numpy as np
    import os
    
    from hsaquery import query, overlaps
    from grizli.pipeline import auto_script
    
    # "Parent" query is grism exposures from the WFC3 ERS program (11359)
    parent = query.run_query(box=None, proposid=[11359], instruments=['WFC3', 'ACS'], extensions=['FLT'], filters=['G102','G141'], extra=[])
    
    # Demo: match everything nearby, includes tons of things from GOODS-S
    extra = query.DEFAULT_EXTRA
    tabs = overlaps.find_overlaps(parent, buffer_arcmin=0.1, filters=[], proposid=[], instruments=['WFC3','ACS'], extra=extra, close=False)
    
    # Match only the grism visit
    extra = query.DEFAULT_EXTRA+["TARGET.TARGET_NAME LIKE 'WFC3-ERSII-G01'"]
    tabs = overlaps.find_overlaps(parent, buffer_arcmin=0.1, filters=['F098M', 'F140W', 'G102', 'G141'], proposid=[11359], instruments=['WFC3'], extra=extra, close=False)
    
    root = 'j033217-274236'
    from grizli.pipeline import auto_script
    auto_script.go(root=root, maglim=[19,20], HOME_PATH='/Volumes/Pegasus/Grizli/DemoERS/')
    
def go(root='j010311+131615', maglim=[17,26], HOME_PATH='/Volumes/Pegasus/Grizli/Automatic', inspect_ramps=False, manual_alignment=False):
    """
    Run the full pipeline for a given target
        
    Parameters
    ----------
    root : str
        Rootname of the `~hsaquery` file.
    
    maglim : [min, max]
        Magnitude limits of objects to extract and fit.
    
    """
    import os
    import glob
    import matplotlib.pyplot as plt

    try:
        from .. import prep, utils
        from . import auto_script
    except:
        from grizli import prep, utils
        from grizli.pipeline import auto_script
        
    #import grizli.utils
    
    roots = [f.split('_info')[0] for f in glob.glob('*dat')]
    
    exptab = utils.GTable.gread(os.path.join(HOME_PATH, '{0}_footprint.fits'.format(root)))
    
    ######################
    ### Download data
    os.chdir(HOME_PATH)
    auto_script.fetch_files(field_root=root, HOME_PATH=HOME_PATH)
    
    if inspect_ramps:
        # Inspect for CR trails
        os.chdir(os.path.join(HOME_PATH, root, 'RAW'))
        os.system("python -c 'from research.grizli.reprocess import inspect; inspect()'")
           
    #######################
    ### Manual alignment
    if manual_alignment:
        os.chdir(os.path.join(HOME_PATH, root, 'Prep'))
        auto_script.manual_alignment(field_root=root, HOME_PATH=HOME_PATH, skip=True)

    #####################
    ### Alignment & mosaics    
    auto_script.preprocess(field_root=root, HOME_PATH=HOME_PATH, make_combined=False)
        
    # Fine alignment
    stop = False
    out = auto_script.fine_alignment(field_root=root, HOME_PATH=HOME_PATH, min_overlap=0.2, stopme=stop, ref_err=0.08, catalogs=['PS1'], NITER=1, maglim=[17,23], shift_only=True, method='Powell', redrizzle=True)
    plt.close()
    
    # Photometric catalogs
    if not stop:
        tab = auto_script.photutils_catalog(field_root=root)
        auto_script.update_grism_wcs_headers(root)
            
    ######################
    ### Grism prep
    os.chdir(os.path.join(HOME_PATH, root, 'Prep'))
    auto_script.grism_prep(field_root=root)
    
    ######################
    ### Grism extractions
    os.chdir(os.path.join(HOME_PATH, root, 'Extractions'))
    auto_script.extract(field_root=root, maglim=maglim, MW_EBV=exptab.meta['MW_EBV'])
    
    ######################
    ### Summary catalog & webpage
    os.chdir(os.path.join(HOME_PATH, root, 'Extractions'))
    auto_script.summary_catalog(field_root=root)
    

def fetch_files(field_root='j142724+334246', HOME_PATH='/Volumes/Pegasus/Grizli/Automatic/', inst_products={'WFPC2/WFPC2': ['C0M', 'C1M'], 'ACS/WFC': ['FLC'], 'WFC3/IR': ['RAW'], 'WFC3/UVIS': ['FLC']}):
    """
    Fully automatic script
    """
    import os
    import glob
    
    try:
        from hsaquery import query, fetch
    except ImportError as ERR:
        warn = """{0}

    Get it from https://github.com/gbrammer/esa-hsaquery""".format(ERR)

        raise(ImportError(warn))
        
    #import grizli
    try:
        from .. import utils
    except:
        from grizli import utils
        
    for dir in [os.path.join(HOME_PATH, field_root), 
                os.path.join(HOME_PATH, field_root, 'RAW'),
                os.path.join(HOME_PATH, field_root, 'Prep'),
                os.path.join(HOME_PATH, field_root, 'Persistence'),
                os.path.join(HOME_PATH, field_root, 'Extractions')]:
        
        if not os.path.exists(dir):
            os.mkdir(dir)
            
    
    tab = utils.GTable.gread('{0}_footprint.fits'.format(field_root))
    tab = tab[(tab['filter'] != 'F218W')]
    if ONLY_F814W:
        tab = tab[(tab['filter'] == 'F814W') | (tab['instdet'] == 'WFC3/IR')]
    
    # Fetch and preprocess IR backgrounds
    os.chdir(os.path.join(HOME_PATH, field_root, 'RAW'))
    
    curl = fetch.make_curl_script(tab, level=None, script_name='fetch_{0}.sh'.format(field_root), inst_products=inst_products, skip_existing=True, output_path='./')
        
    # Ugly callout to shell
    os.system('sh fetch_{0}.sh'.format(field_root))
    files = glob.glob('*raw.fits.gz')
    files.extend(glob.glob('*fl?.fits.gz'))
    for file in files:
        print('gunzip '+file)
        os.system('gunzip {0}'.format(file))
        
    os.system("python -c 'from grizli.pipeline import reprocess; reprocess.reprocess_wfc3ir()'")
    
    # Persistence products
    os.chdir(os.path.join(HOME_PATH, field_root, 'Persistence'))
    persist_files = fetch.persistence_products(tab)
    for file in persist_files:
        if not os.path.exists(os.path.basename(file)):
            print(file)
            os.system('curl -O {0}'.format(file))
    
    for file in persist_files:
        root = os.path.basename(file).split('.tar.gz')[0]
        if os.path.exists(root):
            print('Skip', root)
            continue
            
        # Ugly callout to shell
        os.system('tar xzvf {0}.tar.gz'.format(root))        
        os.system('rm {0}/*extper.fits {0}/*flt_cor.fits'.format(root))
        os.system('ln -sf {0}/*persist.fits ./'.format(root))
      
def manual_alignment(field_root='j151850-813028', HOME_PATH='/Volumes/Pegasus/Grizli/Automatic/', skip=True, radius=5., catalogs=['PS1','SDSS','GAIA','WISE'], radec=None):
    
    import pyds9
    import glob
    import os
    import numpy as np
    
    #import grizli
    from ..prep import get_radec_catalog
    from .. import utils, prep
    
    os.chdir(os.path.join(HOME_PATH, field_root, 'Prep'))
    
    files = glob.glob('*guess')
    if (len(files) > 0) & skip:
        return True
        
    tab = utils.GTable.gread('{0}/{1}_footprint.fits'.format(HOME_PATH, field_root))
    
    files=glob.glob('../RAW/*fl[tc].fits')
    info = utils.get_flt_info(files)
    info = info[(info['FILTER'] != 'G141') & (info['FILTER'] != 'G102')]
    visits, filters = utils.parse_flt_files(info=info, uniquename=True, get_footprint=False)
    
    if radec is None:
        radec, ref_catalog = get_radec_catalog(ra=np.mean(tab['ra']),
                    dec=np.median(tab['dec']), 
                    product=field_root,
                    reference_catalogs=catalogs, radius=radius)
    
    ds9 = pyds9.DS9()
    ds9.set('mode pan')
    ds9.set('scale zscale')
    ds9.set('scale log')
    
    for visit in visits:
        filt = visit['product'].split('-')[-1]
        if (not filt.startswith('g')):
            prep.manual_alignment(visit, reference='{0}_{1}.reg'.format(field_root, ref_catalog.lower()), ds9=ds9)
        
    ds9.set('quit')
    
def preprocess(field_root='j142724+334246', HOME_PATH='/Volumes/Pegasus/Grizli/Automatic/', min_overlap=0.2, make_combined=True, catalogs=['PS1','SDSS','GAIA','WISE']):
    
    import os
    import glob
    import numpy as np
    import grizli

    from shapely.geometry import Polygon
    from scipy.spatial import ConvexHull
    import copy

    #import grizli.prep
    from .. import prep, utils
    
    os.chdir(os.path.join(HOME_PATH, field_root, 'Prep'))
    
    files=glob.glob('../RAW/*fl[tc].fits')
    info = utils.get_flt_info(files)
    #info = info[(info['FILTER'] != 'G141') & (info['FILTER'] != 'G102')]
    
    # Only F814W on ACS
    if ONLY_F814W:
        info = info[((info['INSTRUME'] == 'WFC3') & (info['DETECTOR'] == 'IR')) | (info['FILTER'] == 'F814W')]
    
    visits, filters = utils.parse_flt_files(info=info, uniquename=True, get_footprint=True)
    all_groups = utils.parse_grism_associations(visits)
    
    np.save('{0}_visits.npy'.format(field_root), [visits, all_groups])
    
    # Grism visits
    master_radec = None        
    master_footprint = None
    radec = None
    
    for i in range(len(all_groups)):
        direct = all_groups[i]['direct']
        grism = all_groups[i]['grism']

        print(i, direct['product'], len(direct['files']), grism['product'], len(grism['files']))
        
        if os.path.exists(direct['product']+'_drz_sci.fits'):
            continue
        
        radec = None
        best_overlap = 0
        radec_files = glob.glob('*cat.radec')
        fp = direct['footprint']
        for rdfile in radec_files:
            points = np.loadtxt(rdfile)
            hull = ConvexHull(points)
            rd_fp = Polygon(points[hull.vertices,:])                
            olap = rd_fp.intersection(fp)
            if (olap.area > min_overlap*fp.area) & (olap.area > best_overlap):
                radec = rdfile
                best_overlap = olap.area

        print('\n\n\n{0} radec: {1}\n\n\n'.format(direct['product'], radec))
                        
        # (if you want to run just imaging, say from FFs, use "grism={}")
        status = prep.process_direct_grism_visit(direct=direct, grism=grism,
                            radec=radec, skip_direct=False,
                            align_mag_limits=[14,22],
                            reference_catalogs=catalogs)
    
    # From here, `radec` will be the radec file from the first grism visit
    master_radec = radec
    
    ### Ancillary visits
    imaging_visits = []
    for visit in visits:
        filt = visit['product'].split('-')[-1]
        if (len(glob.glob(visit['product']+'_dr?_sci.fits')) == 0) & (not filt.startswith('g1')):
            imaging_visits.append(visit)
    
    filters = [v['product'].split('-')[-1] for v in visits]
    fwave = np.cast[float]([f.replace('f1','f10').replace('f0','f00').replace('lp','w')[1:-1] for f in filters])
    sort_idx = np.argsort(fwave)[::-1]
    
    for i in sort_idx:
        direct = visits[i]
        if 'g800l' in direct['product']:
            continue
        
        if len(glob.glob(direct['product']+'_dr?_sci.fits')) > 0:
            print('Skip', direct['product'])
            continue
        else:
            print(direct['product'])
        
        radec = None
        best_overlap = 0
        radec_n = 0
        radec_files = glob.glob('*cat.radec')
        fp = direct['footprint']
        for rdfile in radec_files:
            points = np.loadtxt(rdfile)
            hull = ConvexHull(points)
            rd_fp = Polygon(points[hull.vertices,:])                
            olap = rd_fp.intersection(fp)
            if (olap.area > min_overlap*fp.area) & (olap.area > best_overlap) & (len(points) > 0.2*radec_n):
                radec = rdfile
                best_overlap = olap.area
                radec_n = len(points)
                
        print('\n\n\n{0} radec: {1} ({2:.2f})\n\n\n'.format(direct['product'], radec, best_overlap/fp.area))
        
        try:
            try:
                status = prep.process_direct_grism_visit(direct=direct,
                                        grism={}, radec=radec,
                                        skip_direct=False,
                                        run_tweak_align=True,
                                        align_mag_limits=[14,24],
                                        reference_catalogs=catalogs,
                                        align_tolerance=8)
            except:
                status = prep.process_direct_grism_visit(direct=direct,
                                            grism={}, radec=radec,
                                            skip_direct=False,
                                            run_tweak_align=False,
                                            align_mag_limits=[14,24],
                                            reference_catalogs=catalogs,
                                            align_tolerance=8)
                
            failed_file = '%s.failed' %(direct['product'])
            if os.path.exists(failed_file):
                os.remove(failed_file)
            
        except:
            fp = open('%s.failed' %(direct['product']), 'w')
            fp.write('\n')
            fp.close()
    
    ###################################
    # Persistence Masking
    for visit in visits:
        for file in visit['files']:
            print(file)
            if os.path.exists('../Persistence/'+file.replace('_flt', '_persist')):
                prep.apply_persistence_mask(file, path='../Persistence',
                                     dq_value=1024, err_threshold=0.6,
                                     grow_mask=3, verbose=True)
    
    ###################################
    # WFC3/IR Satellite trails
    if False:
        from mywfc3.satdet import _detsat_one
        wfc3 = (info['INSTRUME'] == 'WFC3') & (info['DETECTOR'] == 'IR')
        for file in info['FILE'][wfc3]:
            print(file)
            mask = _detsat_one(file, update=False, ds9=None, plot=False, verbose=True)
        
    ###################################
    # Drizzle by filter
    failed = [f.split('.failed')[0] for f in glob.glob('*failed')]
    keep_visits = []
    for visit in visits:
        if visit['product'] not in failed:
            keep_visits.append(visit)
            
    overlaps = utils.parse_visit_overlaps(keep_visits, buffer=15.0)
    np.save('{0}_overlaps.npy'.format(field_root), [overlaps])
    
    keep = []
    wfc3ir = {'product':'{0}-ir'.format(field_root), 'files':[]}
    
    if not make_combined:
        return True
        
    for overlap in overlaps:
        filt = overlap['product'].split('-')[-1]
        overlap['product'] = '{0}-{1}'.format(field_root, filt)
        
        overlap['reference'] = '{0}-ir_drz_sci.fits'.format(field_root)
        
        if False:
            if 'g1' not in filt:
                keep.append(overlap)
        else:
            keep.append(overlap)
    
        if filt.upper() in ['F098M','F105W','F110W', 'F125W','F140W','F160W']:
            wfc3ir['files'].extend(overlap['files'])

    prep.drizzle_overlaps([wfc3ir], parse_visits=False, pixfrac=0.6, scale=0.06, skysub=False, bits=None, final_wcs=True, final_rot=0, final_outnx=None, final_outny=None, final_ra=None, final_dec=None, final_wht_type='IVM', final_wt_scl='exptime', check_overlaps=False)
                
    prep.drizzle_overlaps(keep, parse_visits=False, pixfrac=0.6, scale=0.06, skysub=False, bits=None, final_wcs=True, final_rot=0, final_outnx=None, final_outny=None, final_ra=None, final_dec=None, final_wht_type='IVM', final_wt_scl='exptime', check_overlaps=False)
            
def photutils_catalog(field_root='j142724+334246', threshold=1.8, subtract_bkg=True):
    """
    Make a detection catalog with SExtractor and then measure
    photometry with `~photutils`.
    """
    import glob
    import numpy as np
    import astropy.io.fits as pyfits
    import astropy.wcs as pywcs
    from photutils import segmentation, background
    import photutils.utils
    
    #import grizli
    #import grizli.prep
    try:
        from .. import prep, utils
    except:
        from grizli import prep, utils
        
    # Photutils catalog
    
    #overlaps = np.load('{0}_overlaps.npy'.format(field_root))[0]
    
    # Make catalog
    sexcat = prep.make_drz_catalog(root='{0}-ir'.format(field_root), threshold=threshold)
    for c in sexcat.colnames:
        sexcat.rename_column(c, c.lower())
    
    sexcat = sexcat['number','mag_auto','flux_radius']

    files=glob.glob('../RAW/*fl[tc].fits')
    info = utils.get_flt_info(files)
    if ONLY_F814W:
        info = info[((info['INSTRUME'] == 'WFC3') & (info['DETECTOR'] == 'IR')) | (info['FILTER'] == 'F814W')]
    
    filters = [f.lower() for f in np.unique(info['FILTER'])]
    
    filters.insert(0, 'ir')
    
    segment_img = pyfits.open('{0}-ir_seg.fits'.format(field_root))[0].data
    
    for ii, filt in enumerate(filters):
        print(filt)
        if filt.startswith('g'):
            continue
        
        if filt not in ['g102','g141']:
            sci_files = glob.glob(('{0}-{1}_dr?_sci.fits'.format(field_root, filt)))
            if len(sci_files) == 0:
                continue
            else:
                sci_file=sci_files[0]
                
            sci = pyfits.open(sci_file)
            wht = pyfits.open(sci_file.replace('_sci','_wht'))
        else:
            continue
        
        photflam = sci[0].header['PHOTFLAM']
        ABZP = (-2.5*np.log10(sci[0].header['PHOTFLAM']) - 21.10 -
                   5*np.log10(sci[0].header['PHOTPLAM']) + 18.6921)
                 
        bkg_err = 1/np.sqrt(wht[0].data)
        bkg_err[~np.isfinite(bkg_err)] = 0#1e30        
        total_error = photutils.utils.calc_total_error(sci[0].data, bkg_err, sci[0].header['EXPTIME'])
        
        wht_mask = (wht[0].data == 0) | (sci[0].data == 0)        
        mask = None #bkg_err > 1.e29
        
        ok = wht[0].data > 0
        if ok.sum() == 0:
            print(' No valid pixels')
            continue
            
        if subtract_bkg:
            bkg = background.Background2D(sci[0].data, 100, mask=wht_mask | (segment_img > 0), filter_size=(3, 3), filter_threshold=None, edge_method='pad')
            bkg_obj = bkg.background
        else:
            bkg_obj = None
            
        cat = segmentation.source_properties(sci[0].data, segment_img, error=total_error, mask=mask, background=bkg_obj, filter_kernel=None, wcs=pywcs.WCS(sci[0].header), labels=None)
        
        if False:
            obj = cat[0]
            seg_cutout = obj.make_cutout(segment_img)
            morph = statmorph.source_morphology(obj.data_cutout, segmap=(seg_cutout == obj.id)*1, variance=obj.error_cutout_ma**2)[0]#, psf=psf)
            
        if filt == 'ir':
            cols = ['id', 'xcentroid', 'ycentroid', 'sky_centroid', 'sky_centroid_icrs', 'source_sum', 'source_sum_err', 'xmin', 'xmax', 'ymin', 'ymax', 'min_value', 'max_value', 'minval_xpos', 'minval_ypos', 'maxval_xpos', 'maxval_ypos', 'area', 'equivalent_radius', 'perimeter', 'semimajor_axis_sigma', 'semiminor_axis_sigma', 'eccentricity', 'orientation', 'ellipticity', 'elongation', 'covar_sigx2', 'covar_sigxy', 'covar_sigy2', 'cxx', 'cxy', 'cyy']
            tab = cat.to_table(columns=cols)
            cols = ['source_sum', 'source_sum_err']
            for c in cols:
                tab[c.replace('sum','flam')] = tab[c]*photflam            
        else:
            cols = ['source_sum', 'source_sum_err']
            t_i = cat.to_table(columns=cols)
            
            mask = (np.isfinite(t_i['source_sum_err']))
            for c in cols:
                tab['{0}_{1}'.format(filt, c)] = t_i[c]
                tab['{0}_{1}'.format(filt, c)][~mask] = np.nan
                cflam = c.replace('sum','flam')
                tab['{0}_{1}'.format(filt, cflam)] = t_i[c]*photflam
                tab['{0}_{1}'.format(filt, cflam)][~mask] = np.nan
                
        tab.meta['PW{0}'.format(filt.upper())] = sci[0].header['PHOTPLAM']
        tab.meta['ZP{0}'.format(filt.upper())] = ABZP
        tab.meta['FL{0}'.format(filt.upper())] = sci[0].header['PHOTFLAM']
                
    icrs = [(coo.ra.value, coo.dec.value) for coo in tab['sky_centroid_icrs']]
    tab['ra'] = [coo[0] for coo in icrs]
    tab['dec'] = [coo[1] for coo in icrs]
    
    tab.remove_column('sky_centroid_icrs')
    tab.remove_column('sky_centroid')
    
    tab.write('{0}_phot.fits'.format(field_root), format='fits', overwrite=True)
    
    return tab
    
def grism_prep(field_root = 'j142724+334246', ds9=None, refine_niter=3):
    import glob
    import os
    import numpy as np
    
    from .. import prep, utils, multifit
    
    files=glob.glob('../RAW/*fl[tc].fits')
    info = utils.get_flt_info(files)
    
    g141 = info['FILTER'] == 'G141'
    g102 = info['FILTER'] == 'G102'
    
    if g141.sum() > 0:
        for f in ['F140W', 'F160W', 'F125W', 'F105W', 'F098M', 'F127M', 'F139M', 'F153M', 'F132N', 'F130N', 'F128N', 'F126N', 'F164N', 'F167N']:
            if f in info['FILTER']:
                g141_ref = f
                break
    
        grp = multifit.GroupFLT(grism_files=list(info['FILE'][g141]), direct_files=[], ref_file='{0}-{1}_drz_sci.fits'.format(field_root, g141_ref.lower()), seg_file='{0}-ir_seg.fits'.format(field_root), catalog='{0}-ir.cat'.format(field_root), cpu_count=-1, sci_extn=1, pad=256)
    
    if g102.sum() > 0:
        for f in ['F105W', 'F098M', 'F125W', 'F140W', 'F160W', 'F127M', 'F139M', 'F153M', 'F132N', 'F130N', 'F128N', 'F126N', 'F164N', 'F167N']:
            if f in info['FILTER']:
                g102_ref = f
                break
    
        grp_i = multifit.GroupFLT(grism_files=list(info['FILE'][g102]), direct_files=[], ref_file='{0}-{1}_drz_sci.fits'.format(field_root, g102_ref.lower()), seg_file='{0}-ir_seg.fits'.format(field_root), catalog='{0}-ir.cat'.format(field_root), cpu_count=-1, sci_extn=1, pad=256)
        if g141.sum() > 0:
            grp.extend(grp_i)
        else:
            grp = grp_i
            
        del(grp_i)
    
    ################
    # Compute preliminary model
    grp.compute_full_model(fit_info=None, verbose=True, store=False, mag_limit=25, coeffs=[1.1, -0.5], cpu_count=4)
        
    ################
    # Remove constant modal background 
    import scipy.stats
    
    for i in range(grp.N):
        mask = (grp.FLTs[i].model < grp.FLTs[i].grism['ERR']*0.6) & (grp.FLTs[i].grism['SCI'] != 0)
        
        # Fit Gaussian to the masked pixel distribution
        clip = np.ones(mask.sum(), dtype=bool)
        for iter in range(3):
            n = scipy.stats.norm.fit(grp.FLTs[i].grism.data['SCI'][mask][clip])
            clip = np.abs(grp.FLTs[i].grism.data['SCI'][mask]) < 3*n[1]
        
        mode = n[0]
        
        print(grp.FLTs[i].grism.parent_file, grp.FLTs[i].grism.filter, mode)
        try:
            ds9.view(grp.FLTs[i].grism['SCI'] - grp.FLTs[i].model)
        except:
            pass
        
        ## Subtract
        grp.FLTs[i].grism.data['SCI'] -= mode
    
    #############
    # Refine the model
    i=0
    if ds9:
        ds9.view(grp.FLTs[i].grism['SCI'] - grp.FLTs[i].model)
        fr = ds9.get('frame')
    
    for iter in range(refine_niter):
        if ds9:
            ds9.set('frame {0}'.format(int(fr)+iter+1))
        
        grp.refine_list(poly_order=3, mag_limits=[19, 24], max_coeff=5, ds9=ds9, verbose=True)

    ##############
    # Save model to avoid having to recompute it again
    grp.save_full_data()
    
    # Link minimal files to Extractions directory
    os.chdir('../Extractions/')
    os.system('ln -s ../Prep/*GrismFLT* .')
    os.system('ln -s ../Prep/*-ir.cat .')
    os.system('ln -s ../Prep/*_phot.fits .')
   
def extract(field_root='j142724+334246', maglim=[13,24], prior=None, MW_EBV=0.00, ids=None):
    import glob
    import os
    
    import numpy as np
    import matplotlib.pyplot as plt
    
    #import grizli
    try:
        from .. import multifit, prep, utils, fitting
    except:
        from grizli import multifit, prep, utils, fitting
        
    grp = multifit.GroupFLT(grism_files=glob.glob('*GrismFLT.fits'), direct_files=[], ref_file=None, seg_file='{0}-ir_seg.fits'.format(field_root), catalog='{0}-ir.cat'.format(field_root), cpu_count=-1, sci_extn=1, pad=256)
    
    ###############
    # PHotometry
    
    target = field_root
    photom = utils.GTable.gread('{0}_phot.fits'.format(target))
    photom_filters = []
    for c in photom.colnames:
        if c.endswith('source_sum') & (c.startswith('f')):
            photom_filters.append(c.split('_source_sum')[0])
    
    photom_flux = np.vstack([photom['{0}_source_flam'.format(f)].data for f in photom_filters])
    photom_err = np.vstack([photom['{0}_source_flam_err'.format(f)].data for f in photom_filters])
    photom_pivot = np.array([photom.meta['PW{0}'.format(f.upper())] for f in photom_filters])
    
    ###########
    # IDs to extract
    #ids=[1096]
    
    if ids is None:
        clip = (grp.catalog['MAG_AUTO'] > maglim[0]) & (grp.catalog['MAG_AUTO'] < maglim[1])
        so = np.argsort(grp.catalog['MAG_AUTO'][clip])
        ids = grp.catalog['NUMBER'][clip][so]
    
    # Stack the different beans
    wave = np.linspace(2000,2.5e4,100)
    poly_templates = utils.polynomial_templates(wave, order=5)
    
    pline = {'kernel': 'point', 'pixfrac': 0.2, 'pixscale': 0.1, 'size': 8, 'wcs': None}
    fsps = True
    t0 = utils.load_templates(fwhm=1000, line_complexes=True, stars=False, full_line_list=None, continuum_list=None, fsps_templates=fsps, alf_template=True)
    t1 = utils.load_templates(fwhm=1000, line_complexes=False, stars=False, full_line_list=None, continuum_list=None, fsps_templates=fsps, alf_template=True)
    
    size = 32
    close = True
    Skip = True
    
    if __name__ == '__main__': # Interactive
        size=32
        close = Skip = False
        
    ###############
    # Stacked spectra
    for id in ids:
        if Skip:
            if os.path.exists('{0}_{1:05d}.stack.png'.format(target, id)):
                continue
            
        beams = grp.get_beams(id, size=size, beam_id='A')
        for i in range(len(beams))[::-1]:
            if beams[i].fit_mask.sum() < 10:
                beams.pop(i)
                
        print(id, len(beams))
        if len(beams) < 1:
            continue
            
        mb = multifit.MultiBeam(beams, fcontam=0.5, group_name=target, psf=False)
        fig1 = mb.oned_figure(figsize=[5,3])
        fig1.savefig('{0}_{1:05d}.1D.png'.format(target, id))
        
        try:
            pfit = mb.template_at_z(z=0, templates=poly_templates, fit_background=True, fitter='lstsq', get_uncertainties=2)
        except:
            pfit = None

        hdu, fig = mb.drizzle_grisms_and_PAs(fcontam=0.5, flambda=False, kernel='point', size=32, zfit=pfit)
        fig.savefig('{0}_{1:05d}.stack.png'.format(target, id))

        hdu.writeto('{0}_{1:05d}.stack.fits'.format(target, id), clobber=True)
        mb.write_master_fits()
        
        if close:
            plt.close(fig); del(hdu); del(mb)
    
    ###############
    # Redshift Fit    
    phot = None
    scale_photometry = False
    fit_beams = True
    zr = [0.1, 3.3]
        
    for id in ids:
        if Skip:
            if os.path.exists('{0}_{1:05d}.line.png'.format(target, id)):
                continue
        
        try:
            out = fitting.run_all(id, t0=t0, t1=t1, fwhm=1200, zr=zr, dz=[0.004, 0.0005], fitter='nnls', group_name=target, fit_stacks=False, prior=prior,  fcontam=0.2, pline=pline, mask_sn_limit=10, fit_beams=False,  root=target+'_', fit_trace_shift=False, phot=phot, verbose=True, scale_photometry=(phot is not None) & (scale_photometry), show_beams=True, overlap_threshold=10, fit_only_beams=True, MW_EBV=MW_EBV)
            mb, st, fit, tfit, line_hdu = out
            
            spectrum_1d = [tfit['cont1d'].wave, tfit['cont1d'].flux]
            grp.compute_single_model(id, mag=-99, size=-1, store=False, spectrum_1d=spectrum_1d, get_beams=None, in_place=True, is_cgs=True)
            
            if True:
                fig = plt.gcf()
                ix = photom['id'] == id
                ax = fig.axes[1]
                ax.errorbar(photom_pivot/1.e4, photom_flux[:,ix].flatten()/1.e-19, photom_err[:,ix].flatten()/1.e-19, color='k', linestyle='None', marker='s', alpha=0.5)
                
                if False:
                     spectrum_1d = [tfit['line1d'].wave, tfit['line1d'].flux]
                     model_mask = mb.get_flat_model(spectrum_1d, apply_mask=True)
                     resid = (mb.scif_mask-model_mask)/mb.sigma_mask
                     
            ######
            # Show the drizzled lines and direct image cutout, which are
            # extensions `DSCI`, `LINE`, etc.
            s, si = 1, 1.6
            fig = fitting.show_drizzled_lines(out[-1], size_arcsec=si, cmap='plasma_r', scale=s, dscale=s)
            fig.savefig('{0}_{1:05d}.line.png'.format(target, id))
                        
            if close:
                for k in range(1000): plt.close()
                
            del(out)
        except:
            pass
    
def summary_catalog(field_root=''):
    """
    Make redshift histogram and summary catalog / HTML table
    """
    import numpy as np
    from matplotlib.ticker import FixedLocator
    import matplotlib.pyplot as plt
    
    from grizli import utils, fitting
    
    ### SUmmary catalog
    fit = fitting.make_summary_catalog(target=field_root, sextractor=None)
    
    clip = (fit['chinu'] < 2.0) & (fit['log_risk'] < -1)
    bins = utils.log_zgrid(zr=[0.1, 3.5], dz=0.02)
    
    
    fig = plt.figure(figsize=[6,4])
    ax = fig.add_subplot(111)
    
    ax.hist(np.log10(1+fit['z_map']), bins=np.log10(1+bins), alpha=0.2, color='k')
    ax.hist(np.log10(1+fit['z_map'][clip]), bins=np.log10(1+bins), alpha=0.8)
    
    xt = np.array(np.arange(0.25, 3.55, 0.25))
    ax.xaxis.set_minor_locator(FixedLocator(np.log10(1+xt)))
    xt = np.array([1,2,3])
    ax.set_xticks(np.log10(1+xt))
    ax.set_xticklabels(xt)
    
    ax.set_xlabel('z')
    ax.set_ylabel(r'$N$')
    
    ax.grid()
    ax.text(0.05, 0.95, field_root, ha='left', va='top', transform=ax.transAxes)
    
    fig.tight_layout(pad=0.2)
    fig.savefig('{0}_zhist.png'.format(field_root))
        
    fit['id','ra', 'dec', 'z_map','log_risk', 'log_pdf_max', 'zq', 'chinu', 'bic_diff', 'png_stack', 'png_full', 'png_line'][clip].write_sortable_html(field_root+'-fit.html', replace_braces=True, localhost=False, max_lines=50000, table_id=None, table_class='display compact', css=None)
    
def fine_alignment(field_root='j142724+334246', HOME_PATH='/Volumes/Pegasus/Grizli/Automatic/', min_overlap=0.2, stopme=False, ref_err = 1.e-3, radec=None, redrizzle=True, shift_only=True, maglim=[17,24], NITER=1, catalogs = ['PS1','SDSS','GAIA','WISE'], method='Powell'):
    """
    Try fine alignment from visit-based SExtractor catalogs
    """    
    import os
    import glob
    import numpy as np
    import matplotlib.pyplot as plt

    from shapely.geometry import Polygon
    from scipy.spatial import ConvexHull
    from drizzlepac import updatehdr
        
    try:
        from .. import prep, utils
        from ..prep import get_radec_catalog
        from ..utils import transform_wcs
    except:
        from grizli import prep, utils
        from grizli.prep import get_radec_catalog
        from grizli.utils import transform_wcs
            
    import astropy.units as u
    import astropy.io.fits as pyfits
    import astropy.wcs as pywcs
    from scipy.optimize import minimize, fmin_powell
    
    import copy
    
    os.chdir(os.path.join(HOME_PATH, field_root, 'Prep'))
    
    files=glob.glob('../RAW/*fl[tc].fits')
    info = utils.get_flt_info(files)
    
    info = info[(info['FILTER'] != 'G141') & (info['FILTER'] != 'G102')]
    
    # Only F814W on ACS
    if ONLY_F814W:
        info = info[((info['INSTRUME'] == 'WFC3') & (info['DETECTOR'] == 'IR')) | (info['FILTER'] == 'F814W')]
    
    all_visits, filters = utils.parse_flt_files(info=info, uniquename=True, get_footprint=False)
    
    visits = []
    files = []
    for visit in all_visits:
        file = '{0}.cat'.format(visit['product'])
        if os.path.exists(file):
            visits.append(visit)
            files.append(file)

    if radec is None:
        radec, ref_catalog = get_radec_catalog(ra=np.mean(info['RA_TARG']),
                    dec=np.median(info['DEC_TARG']), 
                    product=field_root,
                    reference_catalogs=catalogs, radius=5.)
                                 
    #ref = 'j152643+164738_sdss.radec'
    ref_tab = utils.GTable(np.loadtxt(radec, unpack=True).T, names=['ra','dec'])
    
    ridx = np.arange(len(ref_tab))
    
    # Find matches
    tab = {}
    for i, file in enumerate(files):
        tab[i] = {}
        t_i = utils.GTable.gread(file)#, sextractor=True)
        mclip = (t_i['MAG_AUTO'] > maglim[0]) & (t_i['MAG_AUTO'] < maglim[1])
        if mclip.sum() == 0:
            continue
            
        tab[i]['cat'] = t_i[mclip]
        
        sci_file = glob.glob(file.replace('.cat','_dr?_sci.fits'))[0]
        print(sci_file, mclip.sum())
        
        im = pyfits.open(sci_file)
        tab[i]['wcs'] = pywcs.WCS(im[0].header)
        tab[i]['transform'] = [0, 0, 0, 1]
        tab[i]['xy'] = np.array([tab[i]['cat']['X_IMAGE'], tab[i]['cat']['Y_IMAGE']]).T
        
        tab[i]['match_idx'] = {}
        idx, dr = tab[i]['cat'].match_to_catalog_sky(ref_tab)
        clip = dr < 0.6*u.arcsec
        if clip.sum() > 2:
            tab[i]['match_idx'][-1] = [idx[clip], ridx[clip]]
        
        # ix, jx = tab[i]['match_idx'][-1]
        # ci = tab[i]['cat']#[ix]
        # cj = ref_tab#[jx]
            
    for i, file in enumerate(files):
        for j in range(i+1,len(files)):
            sidx = np.arange(len(tab[j]['cat']))
            idx, dr = tab[i]['cat'].match_to_catalog_sky(tab[j]['cat'])
            clip = dr < 0.3*u.arcsec
            print(file, files[j], clip.sum())

            if clip.sum() < 5:
                continue
            
            if clip.sum() > 0:
                tab[i]['match_idx'][j] = [idx[clip], sidx[clip]]
    
    #ref_err = 0.01
        
    #shift_only=True
    if shift_only: 
        p0 = np.vstack([[0,0] for i in tab])
    else:
        p0 = np.vstack([[0,0,0,1] for i in tab])
        
    #ref_err = 0.06

    if False:
        field_args = (tab, ref_tab, ref_err, shift_only, 'field')
        _objfun_align(p0*10., *field_args)
    
    fit_args = (tab, ref_tab, ref_err, shift_only, 'huber')
    plot_args = (tab, ref_tab, ref_err, shift_only, 'plot')
    
    pi = p0*10.
    for iter in range(NITER):
        fit = minimize(_objfun_align, pi*10, args=fit_args, method=method, jac=None, hess=None, hessp=None, bounds=None, constraints=(), tol=None, callback=None, options=None)
        pi = fit.x/10.
        
    ########
    # Show the result
    fig = plt.figure(figsize=[8,4])
    ax = fig.add_subplot(121)
    _objfun_align(p0*10., *plot_args)
    ax.grid()
    ax.set_xlabel('dRA')
    ax.set_ylabel('dDec')
    
    ax = fig.add_subplot(122)
    ax.grid()
    _objfun_align(fit.x, *plot_args)
    ax.set_yticklabels([])
    ax.set_xlabel('dRA')
    fig.tight_layout(pad=0.5)
    
    for ax in fig.axes:
        ax.set_xlim(-0.35, 0.35)
        ax.set_ylim(-0.35, 0.35)

    fig.savefig('{0}_fine.png'.format(field_root))
    np.save('{0}_fine.npy'.format(field_root), [visits, fit])
    
    if stopme:
        return tab, fit, visits
        
    ######### 
    ## Update FLT files
    N = len(tab)
    
    trans = np.reshape(fit.x, (N,-1))/10.
    #trans[0,:] = [0,0,0,1]
    sh = trans.shape
    if sh[1] == 2:
        trans = np.hstack([trans, np.zeros((N,1)), np.ones((N,1))])
    elif sh[1] == 3:
        trans = np.hstack([trans, np.ones((N,1))])
    
    if ref_err > 0.1:
        trans[0,:] = [0,0,0,1]
        
    if not os.path.exists('FineBkup'):
        os.mkdir('FineBkup')
    
    for i in range(N):
        direct = visits[i]
        for file in direct['files']:
            os.system('cp {0} FineBkup/'.format(file))
            print(file)
            
    for ix, i in enumerate(tab):
        direct = visits[ix]
        out_shift, out_rot, out_scale = trans[ix,:2], trans[ix,2], trans[ix,3]
        for file in direct['files']:
            updatehdr.updatewcs_with_shift(file, 
                            str('{0}_wcs.fits'.format(direct['product'])),
                                  xsh=out_shift[0], ysh=out_shift[1],
                                  rot=out_rot, scale=out_scale,
                                  wcsname='FINE', force=True,
                                  reusename=True, verbose=True,
                                  sciext='SCI')
    
        ### Bug in astrodrizzle? Dies if the FLT files don't have MJD-OBS
        ### keywords
        im = pyfits.open(file, mode='update')
        im[0].header['MJD-OBS'] = im[0].header['EXPSTART']
        im.flush()
    
    if redrizzle:
        drizzle_overlaps(field_root)

def update_grism_wcs_headers(field_root):
    """
    Update grism headers with the fine shifts
    """    
    import numpy as np
    #import grizli.prep
    from .. import prep
    
    fine_visits, fine_fit = np.load('{0}_fine.npy'.format(field_root))
    visits, all_groups = np.load('{0}_visits.npy'.format(field_root))
    
    N = len(fine_visits)
    trans = np.reshape(fine_fit.x, (N,-1))/10.
    sh = trans.shape
    if sh[1] == 2:
        trans = np.hstack([trans, np.zeros((N,1)), np.ones((N,1))])
    elif sh[1] == 3:
        trans = np.hstack([trans, np.ones((N,1))])
    
    for i in range(len(all_groups)):
        direct = all_groups[i]['direct']
        grism = all_groups[i]['grism']
        for j in range(N):
            if fine_visits[j]['product'] == direct['product']:
                print(direct['product'], trans[j,:])
                
                prep.match_direct_grism_wcs(direct=direct, grism=grism, get_fresh_flt=False, xyscale=trans[j,:])
                
                
    
def drizzle_overlaps(field_root):
    import numpy as np
    #import grizli
    from .. import prep
    
    ##############
    ## Redrizzle
    overlaps = np.load('{0}_overlaps.npy'.format(field_root))[0]
    keep = []
    wfc3ir = {'product':'{0}-ir'.format(field_root), 'files':[]}
    
    for overlap in overlaps:
        filt = overlap['product'].split('-')[-1]
        overlap['product'] = '{0}-{1}'.format(field_root, filt)
        
        overlap['reference'] = '{0}-ir_drz_sci.fits'.format(field_root)
        
        if False:
            if 'g1' not in filt:
                keep.append(overlap)
        else:
            keep.append(overlap)
    
        if filt.upper() in ['F098M','F105W','F110W', 'F125W','F140W','F160W']:
            wfc3ir['files'].extend(overlap['files'])

    prep.drizzle_overlaps([wfc3ir], parse_visits=False, pixfrac=0.6, scale=0.06, skysub=False, bits=None, final_wcs=True, final_rot=0, final_outnx=None, final_outny=None, final_ra=None, final_dec=None, final_wht_type='IVM', final_wt_scl='exptime', check_overlaps=False)
                
    prep.drizzle_overlaps(keep, parse_visits=False, pixfrac=0.6, scale=0.06, skysub=False, bits=None, final_wcs=True, final_rot=0, final_outnx=None, final_outny=None, final_ra=None, final_dec=None, final_wht_type='IVM', final_wt_scl='exptime', check_overlaps=False)
        
######################
## Objective function for catalog shifts      
def _objfun_align(p0, tab, ref_tab, ref_err, shift_only, ret):
    #from grizli.utils import transform_wcs
    from scipy.special import huber
    import numpy as np
    import matplotlib.pyplot as plt
    
    from ..utils import transform_wcs
    
    N = len(tab)
    
    trans = np.reshape(p0, (N,-1))/10.
    #trans[0,:] = [0,0,0,1]
    sh = trans.shape
    if sh[1] == 2:
        trans = np.hstack([trans, np.zeros((N,1)), np.ones((N,1))])
    elif sh[1] == 3:
        trans = np.hstack([trans, np.ones((N,1))])
        
    #if shift_only:
    #    trans[:,2] = 0.
    #    trans[:,3] = 1.
    
    print(trans)
    
    #N = trans.shape[0]
    trans_wcs = {}
    trans_rd = {}
    for ix, i in enumerate(tab):
        if (ref_err > 0.1) & (ix == 0):
            trans_wcs[i] = transform_wcs(tab[i]['wcs'], translation=[0,0], rotation=0., scale=1.) 
            trans_rd[i] = trans_wcs[i].all_pix2world(tab[i]['xy'], 1)
        else:
            trans_wcs[i] = transform_wcs(tab[i]['wcs'], translation=list(trans[ix,:2]), rotation=trans[ix,2], scale=trans[ix,3]) 
            trans_rd[i] = trans_wcs[i].all_pix2world(tab[i]['xy'], 1) 
    
    # Cosine declination factor
    cosd = np.cos(np.median(trans_rd[i][:,1]/180*np.pi))
    
    if ret == 'field':
        for ix, i in enumerate(tab):
            print(tab[i]['wcs'])
            plt.scatter(trans_rd[i][:,0], trans_rd[i][:,1], alpha=0.8, marker='x')
            continue
            for m in tab[i]['match_idx']:
                ix, jx = tab[i]['match_idx'][m]
                if m < 0:
                    continue
                else:
                    #continue
                    dx_i = (trans_rd[i][ix,0] - trans_rd[m][jx,0])*3600.*cosd
                    dy_i = (trans_rd[i][ix,1] - trans_rd[m][jx,1])*3600.
                    for j in range(len(ix)):
                        if j == 0:
                            p = plt.plot(trans_rd[i][j,0]+np.array([0,dx_i[j]/60.]), trans_rd[i][j,1]+np.array([0,dy_i[j]/60.]), alpha=0.8)
                            c = p[0].get_color()
                        else:
                            p = plt.plot(trans_rd[i][j,0]+np.array([0,dx_i[j]/60.]), trans_rd[i][j,1]+np.array([0,dy_i[j]/60.]), alpha=0.8, color=c)

        return True
    #
    trans_wcs = {}
    trans_rd = {}
    for ix, i in enumerate(tab):
        trans_wcs[i] = transform_wcs(tab[i]['wcs'], translation=list(trans[ix,:2]), rotation=trans[ix,2], scale=trans[ix,3]) 
        trans_rd[i] = trans_wcs[i].all_pix2world(tab[i]['xy'], 1)
                    
    dx, dy = [], []    
    for i in tab:
        mcount = 0
        for m in tab[i]['match_idx']:
            ix, jx = tab[i]['match_idx'][m]
            if m < 0:
                continue
                # 
                # dx_i = (trans_rd[i][ix,0] - ref_tab['ra'][jx])*3600.*cosd
                # dy_i = (trans_rd[i][ix,1] - ref_tab['dec'][jx])*3600.
                # dx.append(dx_i/ref_err)
                # dy.append(dy_i/ref_err)
                # 
                # if ret.startswith('plot'):
                #     plt.gca().scatter(dx_i, dy_i, marker='+', color='k', alpha=0.8, zorder=1000)

            else:
                #continue
                dx_i = (trans_rd[i][ix,0] - trans_rd[m][jx,0])*3600.*cosd
                dy_i = (trans_rd[i][ix,1] - trans_rd[m][jx,1])*3600.
                mcount += len(dx_i)
                dx.append(dx_i/0.01)
                dy.append(dy_i/0.01)                
            
                if ret.startswith('plot'):
                    plt.gca().scatter(dx_i, dy_i, marker='.', alpha=0.1)
        
        if -1 in tab[i]['match_idx']:
            m = -1
            ix, jx = tab[i]['match_idx'][m]
        
            dx_i = (trans_rd[i][ix,0] - ref_tab['ra'][jx])*3600.*cosd
            dy_i = (trans_rd[i][ix,1] - ref_tab['dec'][jx])*3600.
            rcount = len(dx_i)
            mcount = np.maximum(mcount, 1)
            rcount = np.maximum(rcount, 1)
            dx.append(dx_i/(ref_err/np.clip(mcount/rcount, 1, 1000)))
            dy.append(dy_i/(ref_err/np.clip(mcount/rcount, 1, 1000)))

            if ret.startswith('plot') & (ref_err < 0.1):
                plt.gca().scatter(dx_i, dy_i, marker='+', color='k', alpha=0.3, zorder=1000)
            
        
    dr = np.sqrt(np.hstack(dx)**2+np.hstack(dy)**2)
    loss = huber(1, dr).sum()*2
    return loss
        