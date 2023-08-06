"""
Read the FISS fts file and its header.
"""
from __future__ import absolute_import, division

__author__ = "Juhyeong Kang"
__email__ = "jhkang@astro.snu.ac.kr"

from astropy.io import fits
from scipy.signal import savgol_filter
import numpy as np
import os

__all__ = ['frame', 'pca_read', 'raster', 'getheader']

def frame(file,x1=0,x2=False,pca=True,ncoeff=False,xmax=True,
          smooth=False,**kwargs):
    """Read the FISS fts file.

    Parameters
    ----------
    file : str
        A string of file name to be read.
    x1 : int
        A starting index of the frame along the scanning direction.
    x2 : (optional) int
        An ending index of the frame along the scanning direction.
        If not, then the only x1 frame is read.
    pca : (optional) bool
        If True, the frame is read from the PCA file.
        Default is True, but the function automatically check
        the existance of the pca file.
    ncoeff : (optional) int
        The number of coefficients to be used for
        the construction of frame in a pca file.
    xmax : (optional) bool
        If True, the x2 value is set as the maximum end point of the frame.
            * Default is False.
    smooth : (optional) bool
        If True, apply the Savitzky-Golay filter to increase the signal to
        noise without greatly distorting the signal of the given fts file.
            * Default is False.
    nsmooth : (optional) int
        The number of smooting.
        Default is 1 for the case of the compressed file,
        and is 2 for the case of the uncompresseed file.
    kwargs 
        The parameters for smooth (savitzky-golay filter), \n
        See the docstring of the `scipy.signal.savgol_filter`.
        
    Returns
    -------
    frame : ~numpy.ndarray
        FISS data frame with the information of (wavelength, y, x).

    References
    ----------
    `Savitzky-Golay filter <https://en.wikipedia.org/wiki/Savitzky%E2%80%93Golay_filter>`_.\n
    `scipy.signal.savgol_filter <https://docs.scipy.org/doc/scipy-0.18.1/reference/generated/scipy.signal.savgol_filter.html#scipy.signal.savgol_filter>`_
    
    Notes
    -----
        This function is based on the IDL code FISS_READ_FRAME.PRO 
        written by J. Chae, 2013.
    
        This function automatically check the existance of the pca
        file by reading the fts header.
        
    Example
    -------
    .. plot::
        :include-source:
            
        import matplotlib.pyplot as plt
        from fisspy.io import read
        import fisspy
        import fisspy.data.sample
        data=read.frame(fisspy.data.sample.FISS_IMAGE,xmax=True)
        plt.imshow(data[:,75],cmap=fisspy.cm.ca,origin='lower',interpolation='bilinear')
        plt.title(r"GST/FISS 8542 $\AA$ Spectrogram")
        plt.show()
    """
    if not file:
        raise ValueError('Empty filename')
    if x2 and x2 <= x1:
        raise ValueError('x2 must be larger than x1')
    
    header=fits.getheader(file)
    
    try:
        header['pfile']
    except:
        pca=False
    
    if xmax:
        x2=header['naxis3']
    elif not x2:
        x2=x1+1
    
    if pca:
        spec=pca_read(file,header,x1,x2,ncoeff=ncoeff)
    else:        
        spec=fits.getdata(file)[x1:x2]
    if x1+1 == x2:
        spec=spec[0]
        return spec
    spec=spec.transpose((1,0,2)).astype(float)
    
    if smooth:
        winl=kwargs.pop('window_length',7)
        pord=kwargs.pop('polyorder',3)
        deriv=kwargs.pop('deriv',0)
        delta=kwargs.pop('delta',1.0)
        mode=kwargs.pop('mode','interp')
        cval=kwargs.pop('cval',0.0)
        nsmooth=kwargs.pop('nsmooth',int(not pca)+1)
            
        for i in range(nsmooth):
            spec=savgol_filter(spec,winl,pord,deriv=deriv,
                               delta=delta,mode=mode,cval=cval)
    return spec


def pca_read(file,header,x1,x2=False,ncoeff=False):
    """
    Read the pca compressed FISS fts file.
    
    Parameters
    ----------
    file : str
        A string of file name to be read.
    header : astropy.io.fits.header.Header
        The fts file header.
    x1   : int
        A starting index of the frame along the scanning direction.
    x2   : (optional) int
        An ending index of the frame along the scanning direction.
        If not, then the only x1 frame is read.
    ncoeff : (optional) int
        The number of coefficients to be used for
        the construction of frame in a pca file.
    
    Returns
    -------
    frame : ~numpy.ndarry
        FISS data frame with the information of (wavelength, y, x).
        
    Notes
    -----
        This function is based on the IDL code FISS_PCA_READ.PRO
        written by J. Chae, 2013.
        The required fts data are two. One is the "_c.fts",
        and the other is "_p.fts"
    
    """
    if not file:
        raise ValueError('Empty filename')
    if not x2:
        x2=x1+1
        
    dir=os.path.dirname(file)
    pfile=header['pfile']
    
    if dir:
        pfile=dir+os.sep+pfile
        
    pdata=fits.getdata(pfile)
    data=fits.getdata(file)[x1:x2]
    ncoeff1=data.shape[2]-1
    if not ncoeff:
        ncoeff=ncoeff1
    elif ncoeff > ncoeff1:
        ncoeff=ncoeff1
    
    spec=np.dot(data[:,:,0:ncoeff],pdata[0:ncoeff,:])
    spec*=10.**data[:,:,ncoeff][:,:,None]
    return spec

def raster(file,wv,hw=0.05,x1=0,x2=False,y1=0,y2=False,pca=True,
           smooth=False,**kwargs):
    """
    Make raster images for a given file at wv of wavelength within width hw
    
    Parameters
    ----------
    file : str
        A string of file name to be read.
    wv   : float or 1d ndarray
        Referenced wavelengths.
    hw   : float
        A half-width of wavelength integration in unit of Angstrom.
        Default is 0.05
    x1   : (optional) int
        A starting index of the frame along the scanning direction.
    x2   : (optional) int
        An ending index of the frame along the scanning direction.
        If not, x2 is set to the maximum end point of the frame.
    y1   : (optional) int
        A starting index of the frame along the slit position.
    y2   : (optional0 int
        A ending index of the frame along the slit position.
    pca  : (optional) bool
        If True, the frame is read from the PCA file.
        Default is True, but the function automatically check
        the existance of the pca file.
    smooth : (optional) bool
        If True, apply the Savitzky-Golay filter to increase the signal to
        noise without greatly distorting the signal of the given fts file.
            * Default is False.
    kwargs
        Any additional keyword arguments to read frame.
        See the docstring of `fisspy.io.read.frame`
        
    Returns
    -------
    Raster : ~numpy.ndarray
        Raster image at given wavelengths.
        
    Notes
    -----
        This function is based on the IDL code FISS_RASTER.PRO
        written by J. Chae, 2013.
        This function automatically check the existance of the pca file by
        reading the fts header.
    
    Example
    -------
    .. plot::
        :include-source:
            
        import matplotlib.pyplot as plt
        from fisspy.io import read
        import fisspy
        import fisspy.data.sample
        raster=read.raster(fisspy.data.sample.FISS_IMAGE,0.3)
        plt.imshow(raster,cmap=fisspy.cm.ca,origin='lower',interpolation='bilinear')
        plt.title(r"GST/FISS 8542+0.3 $\AA$ Spectrogram")
        plt.show()
    """
    header=getheader(file,pca)
    nw=header['NAXIS1']
    ny=header['NAXIS2']
    nx=header['NAXIS3']
    wc=header['CRPIX1']
    dldw=header['CDELT1']
    
    if not file:
        raise ValueError('Empty filename')
    if x2 and x2 <= x1+1:
        raise ValueError('x2 must be larger than x1+1')
    
    try:
        num=wv.shape[0]    
    except:
        num=1
        wv=np.array([wv])
    
    if not x2:
        x2=int(nx)
    if not y2:
        y2=int(ny)
    
    wl=(np.arange(nw)-wc)*dldw
    if hw < abs(dldw)/2.:
        hw=abs(dldw)/2.
    
    s=np.abs(wl-wv[:,None])<=hw
    sp=frame(file,x1,x2,pca=pca,smooth=smooth,**kwargs)
    leng=s.sum(1)
    if num == 1:
        img=sp[y1:y2,:,s[0,:]].sum(2)/leng[0]
        return img.reshape((y2-y1,x2-x1))
    else:
        img=np.array([sp[y1:y2,:,s[i,:]].sum(2)/leng[i] for i in range(num)])
        return img.reshape((num,y2-y1,x2-x1))


def getheader(file,pca=True):
    """
    Get the FISS fts file header.
    
    Parameters
    ----------
    file : str
        A string of file name to be read.
    pca  : (optional) bool
        If True, the frame is read from the PCA file.
        Default is True, but the function automatically check
        the existance of the pca file.
    
    Returns
    -------
    header : astropy.io.fits.Header
        The fts file header.
    
    Notes
    -----
        This function automatically check the existance of the pca file by
        reading the fts header.
    
    Example
    -------
    >>> from fisspy.io import read
    >>> h=read.getheader(file)
    >>> h['date']
    '2014-06-03T16:49:42'
    """
    header0=fits.getheader(file)
    
    pfile=header0.pop('pfile',False)
    if not pfile:
        return header0
        
    header=fits.Header()
    if pca:
        header['pfile']=pfile
        for i in header0['comment']:
            sori = i.split('=')
            if len(sori) == 1:
                skv = sori[0].split(None,1)
                if len(skv) == 1:
                    pass
                else:
                    header[skv[0]] = skv[1]
            else:
                key = sori[0]
                svc = sori[1].split('/')
                try:
                    item=float(svc[0])
                except:
                    item=svc[0].split("'")
                    if len(item) != 1:
                        item=item[1].split(None,0)[0]
                    else:
                        item=item[0].split(None,0)[0]
                try:
                    if item-int(svc[0]) == 0:
                        item=int(item)
                except:
                    pass
                if len(svc) == 1:
                    header[key]=item
                else:
                    header[key]=(item,svc[1])
                    
    header['simple']=True
    alignl=header0.pop('alignl',-1)
    
    if alignl == 0:
        keys=['reflect','reffr','reffi','cdelt2','cdelt3','crota2',
              'crpix3','shift3','crpix2','shift2','margin2','margin3']
        header['alignl']=(alignl,'Alignment level')
        for i in keys:
            header[i]=(header0[i],header0.comments[i])
        header['history']=str(header0['history'])
    if alignl == 1:
        keys=['reflect','reffr','reffi','cdelt2','cdelt3','crota1',
              'crota2','crpix3','crval3','shift3','crpix2','crval2',
              'shift2','margin2','margin3']
        header['alignl']=(alignl,'Alignment level')
        for i in keys:
            header[i]=(header0[i],header0.comments[i])
        header['history']=str(header0['history'])
        
    return header
