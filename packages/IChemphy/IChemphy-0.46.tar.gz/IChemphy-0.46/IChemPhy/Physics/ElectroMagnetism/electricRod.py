def ElectricRod():

    import numpy as np
    import math
    import collections
    from mpl_toolkits.mplot3d import Axes3D
    import matplotlib.pyplot as plt
    from matplotlib import cm
    from matplotlib.ticker import LinearLocator, FormatStrFormatter

    k=9.0 *(math.pow(10,9))
    Q = int(input('Enter charge of rod:'))
    L = int(input('Enter length of rod:'))

    def E(xd, yd):
        y = yd#float(input('Enter the y-cord of the particle: '))
        x = xd 
    
        #r= math.pow(x**2+(y-L)**2,0.5)
        ab=((x**2)*(math.pow((L**2-4*L*y+4*(x**2+y**2)),0.5)))
        ba = ((x**2)*(math.pow(L**2+4*L*y+4*(x**2+y**2),0.5)))
    
        E_xComponent = (k*x/L)*(((L-2*y)/ab)+ ((L+2*y)/ba))
        E_yComponent = (k/L)*((L*y) - (((L-2*y)*y -2*(x**2))/ab) + (((L+2*y)*y +2*(x**2))/ba))
        #E_xComponent = k*2*L*x*Q/((x**2+y)*(math.pow(-(L**2)+ 4*((x**2)+y), 0.5)))
        #E_yComponent = k*2*L*y*Q/((x**2+y)*(math.pow(-(L**2)+ 4*((x**2)+y), 0.5)))
    
        Strength_ElectricField = math.pow((E_xComponent**2+ E_yComponent**2), 0.5)
        #Strength_ElectricFiled = k* Q/(r*(math.pow(r**2+(L/2)**2,0.5)))

        tan_theta= E_yComponent/E_xComponent
    
    #     if tan_theta>0:
    #         return Strength_ElectricField   
    #     else:
    #          return -1*Strength_ElectricField   
   
        return Strength_ElectricField  


    NN=0.01
    #xdist= np.append(np.arange(-4*L, -NN,(4*L-NN)/100),np.arange(NN, 4*L,(4*L-NN)/100)).flatten()
    #ydist= np.append(np.arange(-L/2, -NN,(L/2-NN)/100),np.arange(NN, L/2,(L/2-NN)/100)).flatten() 
    LL=1
    NL=100
    xdist= np.append(np.arange(-4*LL, -NN,(4*LL-NN)/NL),np.arange(NN, 4*LL,(4*LL-NN)/NL)).flatten()
    ydist= np.append(np.arange(-LL/2, -NN,(LL/2-NN)/NL),np.arange(NN, LL/2,(LL/2-NN)/NL)).flatten()
    matrix = [[0 for i in range(len(xdist))] for j in range(len(ydist))]


    for i in range(len(xdist)-1):
        for j in range(len(ydist)-1):
            #if 4*(xdist[i]*xdist[i]+ydist[j])>L**2:
                 matrix[i][j]= E(xdist[i],ydist[j])
            
    matrix = np.array(matrix)

    np.append(np.arange(-4*L, -0.1,8*L/100),np.arange(0.1, 4*L,8*L/100)).flatten()
    print(matrix)

    import pylab as plt
    import numpy as np
    #plt.ylim(-5*(math.pow(10,6)),math.pow(10,7))
    #fig = plt.figure(figsize=(10,4))
    fig = plt.figure()
    ax = fig.gca(projection='3d')
    X, Y = np.meshgrid(xdist, ydist)
    #fig.suptitle('test title', fontsize=20)
    plt.xlabel('x - coordinate', fontsize=8)
    plt.ylabel('y - coordinate', fontsize=8)
    surf = ax.plot_surface(X, Y,matrix, cmap=cm.coolwarm,linewidth=0, antialiased=False)

    # Customize the z axis.
    #ax.set_zlim(-1.01, 1.01)
    ax.zaxis.set_major_locator(LinearLocator(10))
    #ax.zaxis.set_major_formatter(FormatStrFormatter('%.02f'))

    # Add a color bar which maps values to colors.
    fig.colorbar(surf, shrink=0.5, aspect=5)

    plt.show()





    plt.pcolormesh(xdist, ydist, matrix)
    plt.colorbar() #need a colorbar to show the intensity scale
    plt.show()

    plt.pcolormesh(xdist, ydist, matrix)
    plt.colorbar() #need a colorbar to show the intensity scale
    plt.show()

    import pylab as plt
    import numpy as np

    # Sample data
    X,Y = np.meshgrid(xdist, ydist)
    Z = matrix


    # Plot the density map using nearest-neighbor interpolation
    plt.pcolormesh(X,Y,Z)

    plt.show


