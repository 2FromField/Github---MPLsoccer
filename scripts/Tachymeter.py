def tachymeter(value,max_value,n_zone,title=None, unit=None):
    """Return a tachymeter with the needle placed according to the given percentage

    Args:
        value (float): current value to exposed
        max_value (float): maximum reference value 
        n_zone (int): number of areas to be imaged (0 to 7)
        title (str): title of the tachymeter
    """
    import numpy as np
    import matplotlib.pyplot as plt
    
    seuils = {
    0:[{'upper_zone':[0]},{'upper_zone_color':['']}],
    1:[{'upper_zone':[1,1]},{'upper_zone_color':['green','#999999']}],
    2:[{'upper_zone':[1,1,2]},{'upper_zone_color':['red','green','#999999']}],
    3:[{'upper_zone':[1,1,1,3]},{'upper_zone_color':['red','orange','green','#999999']}],
    4:[{'upper_zone':[1,1,1,1,4]},{'upper_zone_color':['red','orange','yellow','green','#999999']}],
    5:[{'upper_zone':[1,1,1,1,1,5]},{'upper_zone_color':['red','orange','yellow','lightgreen','green','#999999']}],
    6:[{'upper_zone':[1,1,1,1,1,1,6]},{'upper_zone_color':['firebrick','red','orange','yellow','lightgreen','green','#999999']}],
    7:[{'upper_zone':[1,1,1,1,1,1,1,7]},{'upper_zone_color':['firebrick','red','orange','gold','yellow','lightgreen','green','#999999']}],
                }

    for cle_seuil,value_seuil in seuils.items():
        if cle_seuil == n_zone:
            upper_zone = value_seuil[0]['upper_zone']
            upper_zone_color = value_seuil[1]['upper_zone_color']
    
    # Calcul of the percentage
    percentage = (value*100)/max_value
    
    # Title positionning
    title_postion = -0.1
    for i in np.arange(5,100,7):
        if len(title) > i:
            print(i)
            title_postion += -0.1
        else:
            break


    # Create the zones and the needle
    under_zone = [percentage,1*1,100+(100-percentage)]

    # plot
    n = plt.figure(facecolor='#1a211f')
    n = plt.pie(upper_zone, colors=upper_zone_color,
        wedgeprops={"linewidth": 1, "edgecolor": "#1a211f"}, frame=True)
    n[0][len(upper_zone_color)-1].set_alpha(0.0)
    
    n = plt.pie(under_zone, colors=['#999999','white','#999999'],
        wedgeprops={"linewidth": 1, "edgecolor": "white"}, frame=True)
    n[0][0].set_alpha(0.0)
    n[0][2].set_alpha(0.0)
    plt.text(-0.1,-0.2,f'{value} {unit}',fontweight='bold',c='white')
    plt.text(title_postion,-0.4,f'{title}',fontweight='bold',c='white')
    plt.subplots_adjust(left=0,bottom=0,right=1,top=1)
    n=plt.axis('off')

    plt.show()


tachymeter(value=23, max_value=80, n_zone=6, title='Testing Tachymeter', unit='cm')