import cv2
import numpy
import os

def deteccio(filename, p1, p2):

    # Carregem l'imatge
    image = cv2.imread(filename)

    # Guardo el path per despres poder guardar l'imatge processada
    head, tail = os.path.split(filename)

    #Fem una copia on posarem els contorns que trobem per no destroçar l'original
    output = image.copy()

    # Canviem de RGB a escala de grisos ja que la funcio que utlitzem ho necessita.
    gray  = cv2.cvtColor(image, cv2.COLOR_BGR2GRAY)

    # HoughCircles es la funcio de opencv que serveix per buscar contorns circulars en una imatge
    circles = cv2.HoughCircles(gray, cv2.HOUGH_GRADIENT, float(p1), int(p2), maxRadius=200)

    # Preparem el contador de cercles trobats i la font amb la que posarem les coordenades a l'imatge
    font = cv2.FONT_HERSHEY_SIMPLEX
    cont = 0


    if circles is not None:
        # Pasem les coordenades que trobem a integer
        circles = numpy.round(circles[0, :]).astype("int")

        for (x, y, r) in circles:
            # Dibuixem els cercles que hem trobat i el centre
            cv2.circle(output, (x, y), r, (0, 255, 0), 4)
            cv2.rectangle(output, (x - 5, y - 5), (x + 5, y + 5), (0, 128, 255), -1)
            # Mostrem el contador i les coordenades
            cv2.putText(output, str(cont) + " (x: " + str(x) + ", y: " + str(y) + ")", (x + 10, y + 10), font, 0.5, (255, 255, 255), 1)
            cont = cont+1

        imProPath = os.path.join(head, 'ProcessedImage.jpg')
        cv2.imwrite(imProPath, output)
        return 0, imProPath, circles

    else:
        return 1, None, None


def deteccio2():
    """
    Aquesta funcio serveix per detectar els contorns de les peces sense coneixer el fons, distinguim utilitzant un threshold.
    Treballem la imatge en escala de grisos.
    TODO: ELS CONTORNS RODONS S'HAN DE MILLORAR
        LES IMATGES MOLT GRANS (LES FETES AMB EL MOVIL, TENEN MOLTS PROBLEMES PER TROBAR COSES)
    Avantatges: Es mes adapatable a les diferents situacions d'il·luminacio
    Desavanatges: No es molt fiable si no hi ha un bon contrast entre l'objecte i el fons
    :return:
    """

    """
    THRESHOLDS:
        shapes.PNG - 240
        shapes.jpg - 240
        random.jpg - 190 / 200
        billar.png - 110
    """

    #Carregem l'imatge i la transformem a escala de grisos
    im = cv2.imread('lab1.jpeg')
    if im is None:
        print("Error: No s'ha pogut carregar l'imatge")
        quit()
    imGrey = cv2.cvtColor(im, cv2.COLOR_BGR2GRAY)

    # el _ es perque no volem el primer valor retornat per la funcio
    _, thresh = cv2.threshold(imGrey, 200, 255, cv2.THRESH_BINARY)

    # Busquem els contorns
    contours, _ = cv2.findContours(thresh, cv2.RETR_TREE, cv2.CHAIN_APPROX_NONE)

    
    for contour in contours:
        # Aquests metode aproxima quina es la forma del contorn. Arc length calcula el perimetre del contorn. Els True es perque els contorns que tenim sabem que son tancats
        approx = cv2.approxPolyDP(contour, 0.01*cv2.arcLength(contour, True), True)
        cv2.drawContours(im, [approx], 0, (0, 0, 0), 2)
    """
        x = approx.ravel()[0]
        y = approx.ravel()[1]
        if len(approx) == 3: # Els triangles son amb 3 rectes
            cv2.putText(im, "Triangle", (x, y), cv2.FONT_HERSHEY_COMPLEX, 0.2, (0, 0, 0)) # (0,0,0) es el color negre
        elif len(approx) == 4:
            x , y, w, h = cv2.boundingRect(approx)
            aspectRatio = float(w)/h
            # Suposant que hi ha soroll
            if aspectRatio >= 0.95 and aspectRatio <= 1.05:
                cv2.putText(im, "Quadrat", (x, y), cv2.FONT_HERSHEY_COMPLEX, 0.5, (0, 0, 0))
            else:
                cv2.putText(im, "Rectangle", (x, y), cv2.FONT_HERSHEY_COMPLEX, 0.5, (0, 0, 0))
        elif len(approx) == 5:
            cv2.putText(im, "Pentagon", (x, y), cv2.FONT_HERSHEY_COMPLEX, 0.5, (0, 0, 0))
        elif len(approx) == 10:
            cv2.putText(im, "Estrella", (x, y), cv2.FONT_HERSHEY_COMPLEX, 0.5, (0, 0, 0))
        else:
            cv2.putText(im, "Cercle", (x, y), cv2.FONT_HERSHEY_COMPLEX, 0.5, (0, 0, 0))
    """

    cv2.imshow("Shapes", im)

    # Sortir amb la tecla ESC
    while (1):
        tecla = cv2.waitKey(5) & 0xFF
        if tecla == 27:
            break

    # Eliminar la finestra que es crea per la imatge
    cv2.destroyAllWindows()
    quit()



def deteccio3():

    # Carregem l'imatge
    image = cv2.imread("im2_l.jpg")

    cv2.imshow("original", image)
    cv2.waitKey(0)

    #Fem una copia on posarem els contorns que trobem per no destroçar l'original
    output = image.copy()

    # Canviem de RGB a escala de grisos ja que la funcio que utlitzem ho necessita.
    gray  = cv2.cvtColor(image, cv2.COLOR_BGR2GRAY)

    # HoughCircles es la funcio de opencv que serveix per buscar contorns circulars en una imatge
    circles = cv2.HoughCircles(gray, cv2.HOUGH_GRADIENT, 1.6, 180, maxRadius=200)

    # Preparem el contador de cercles trobats i la font amb la que posarem les coordenades a l'imatge
    font = cv2.FONT_HERSHEY_SIMPLEX
    cont = 0


    if circles is not None:
        # Pasem les coordenades que trobem a integer
        circles = numpy.round(circles[0, :]).astype("int")

        for (x, y, r) in circles:
            # Dibuixem els cercles que hem trobat i el centre
            cv2.circle(output, (x, y), r, (0, 255, 0), 4)
            cv2.rectangle(output, (x - 5, y - 5), (x + 5, y + 5), (0, 128, 255), -1)
            # Mostrem el contador i les coordenades
            cv2.putText(output, str(cont) + " (x: " + str(x) + ", y: " + str(y) + ")", (x + 10, y + 10), font, 0.5, (255, 255, 255), 1)
            cont = cont+1

        # show the output image
        cv2.imshow("output", output)
        cv2.waitKey(0)

    else:
        print("No circles detected")

def deteccio3():

    # Carregem l'imatge
    image = cv2.imread("im1_sl.jpg")

    cv2.imshow("original", image)
    cv2.waitKey(0)

    #Fem una copia on posarem els contorns que trobem per no destroçar l'original
    output = image.copy()

    # Canviem de RGB a escala de grisos ja que la funcio que utlitzem ho necessita.
    gray  = cv2.cvtColor(image, cv2.COLOR_BGR2GRAY)

    # HoughCircles es la funcio de opencv que serveix per buscar contorns circulars en una imatge
    circles = cv2.HoughCircles(gray, cv2.HOUGH_GRADIENT, 1.6, 180, maxRadius=200)

    # Preparem el contador de cercles trobats i la font amb la que posarem les coordenades a l'imatge
    font = cv2.FONT_HERSHEY_SIMPLEX
    cont = 0


    if circles is not None:
        # Pasem les coordenades que trobem a integer
        circles = numpy.round(circles[0, :]).astype("int")

        for (x, y, r) in circles:
            # Dibuixem els cercles que hem trobat i el centre
            cv2.circle(output, (x, y), r, (0, 255, 0), 4)
            cv2.rectangle(output, (x - 5, y - 5), (x + 5, y + 5), (0, 128, 255), -1)
            # Mostrem el contador i les coordenades
            cv2.putText(output, str(cont) + " (x: " + str(x) + ", y: " + str(y) + ")", (x + 10, y + 10), font, 0.5, (255, 255, 255), 1)
            cont = cont+1

        # show the output image
        cv2.imshow("output", output)
        cv2.waitKey(0)

    else:
        print("No circles detected")


if __name__ == "__main__":

    #deteccio()

    #deteccio2()

    deteccio3()