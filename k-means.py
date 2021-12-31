import pygame
from random import randint
from math import sqrt
from sklearn.cluster import KMeans

pygame.init()
screen = pygame.display.set_mode((700,900))
pygame.display.set_caption('KNN algo visualization')

panel_width = 700
panel_height = 700

running = True
tick = pygame.time.Clock()

font = pygame.font.SysFont('sans', 35)
font_small = pygame.font.SysFont('sans', 20)
background = (176,224,230)
BLACK = (0,0,0)
WHITE = (254,254,254)
LEMON_CHIFFON = (255,250,205)
BLUE = (0,0,255)
RED = (255,0,0)
GREEN = (0,255,0)
YELLOW = (255,215,0)
PINK = (255,20,147)
DARK_BLUE = (0,51,102)

points = []
k_num = 0
error = 0
clusters = []
labels =[]
colors = [BLUE, RED, GREEN, YELLOW, PINK, DARK_BLUE]
algo_clicked = False

def distance(point1, point2) -> float:
	return sqrt((point1[0]-point2[0])**2 + (point1[1]-point2[1])**2)

while running:
	tick.tick(60)
	screen.fill(background)
	mouse_x, mouse_y = pygame.mouse.get_pos()

	# Start Draw Interface

	## Draw text 
	pygame.draw.rect(screen, LEMON_CHIFFON, (0,701, 700,900))
	text = font.render("Clusters K = " + str(k_num), True, BLACK)
	screen.blit(text, (60,760))


	## Draw Black Rects
	pygame.draw.rect(screen, BLACK, (390,720, 50,50))
	plus = font.render('+', True, WHITE)
	screen.blit(plus, (407,725))

	pygame.draw.rect(screen, BLACK, (490,720, 50,50))
	minus = font.render('_', True, WHITE)
	screen.blit(minus, (507,710))

	pygame.draw.rect(screen, BLACK, (390,780, 150,50))
	text = font_small.render('Random', True, WHITE)
	screen.blit(text, (435,793))

	pygame.draw.rect(screen, BLACK, (390,840, 150,50))
	text = font_small.render('Run', True, WHITE)
	screen.blit(text, (450,853))

	pygame.draw.rect(screen, BLACK, (545,780, 150,110))
	text = font_small.render("""Check Algorithm""", True, WHITE)
	screen.blit(text, (560,825))


	## Mouse position
	if mouse_x < panel_width and mouse_y <= panel_height:
		text_mouse = font_small.render( "(" + str(mouse_x) + ',' + str(mouse_y) + ')' , True, BLACK)
		if (mouse_x >666 and mouse_y > 618) or (mouse_x >618):
			screen.blit(text_mouse, (mouse_x-70, mouse_y-20))
		elif mouse_y >666: 
			screen.blit(text_mouse, (mouse_x+10, mouse_y-20))
		else:
			screen.blit(text_mouse, (mouse_x+10, mouse_y+10))



	# End Draw Interface

	for event in pygame.event.get():
		#Close window
		if event.type == pygame.QUIT:
			running = False

		# Check clicked
		if event.type == pygame.MOUSEBUTTONDOWN:
			### Check plus and minus button clicked
			if 390<mouse_x<390+50 and 720<mouse_y<720+50 and k_num<6: # Max K = 6 
				k_num+=1
			if 490<mouse_x<490+50 and 720<mouse_y<720+50 and k_num>0:
				k_num-=1

			### Check mouse in draw panel
			if mouse_y <= panel_height:
				labels = []
				points.append([mouse_x, mouse_y])

			### Check Random button clicked
			if 390<mouse_x<390+150 and 780<mouse_y<780+50:
				clusters = []
				labels = []
				for i in range(k_num):
					clusters.append([randint(0, 700), randint(0, 700)])

			### Check Run button clicked
			if 390<mouse_x<390+150 and 840<mouse_y<840+50:
				if clusters == []:
					continue
				labels =[]
				for point in points:
					dis_point_clus = []
					for clus in clusters:
						dis_point_clus.append(distance(point, clus))
					labels.append(dis_point_clus.index(min(dis_point_clus)))

				#### Move cluster point
				for i in range(k_num):
					sum_x = 0
					sum_y = 0
					count = 0
					for j in range(len(points)):
						if labels[j] == i:
							sum_x += points[j][0]
							sum_y += points[j][1]
							count += 1

					if count != 0:
						clusters[i] = [int(sum_x/count), int(sum_y/count)]


			### Check Algorithm button clicked
			if 545<mouse_x<545+150 and 780<mouse_y<780+110:
				algo_clicked = True
				if k_num == 0:
					continue
				kmeans = KMeans(n_clusters= k_num).fit(points)
				clusters = kmeans.cluster_centers_
				labels = kmeans.labels_
				error = int(kmeans.inertia_)
				text = font.render("ERROR = " + str(error), True, BLACK)
				screen.blit(text, (60,830))


	### find total error
	error = 0
	if (clusters != []) and (labels !=[]):
		for i in range(len(points)):
			error += int(distance(points[i], clusters[labels[i]]))
	text = font.render("ERROR = " + str(error), True, BLACK)
	screen.blit(text, (60,830))



	# Draw points:
	for i in range(len(points)):
		pygame.draw.circle(screen, BLACK, (points[i]), 6)
		if labels == []:
			pygame.draw.circle(screen, WHITE, (points[i]), 5)
		else: pygame.draw.circle(screen, colors[labels[i]], (points[i]), 5)


	for i in range(len(clusters)):
		pygame.draw.circle(screen, BLACK, (clusters[i]), 7)
		pygame.draw.circle(screen, colors[i], (clusters[i]), 8)

	pygame.display.flip()
pygame.quit()