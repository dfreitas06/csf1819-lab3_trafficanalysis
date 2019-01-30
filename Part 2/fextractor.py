import os
import argparse
import math

#CSF1819: 
    #Here you should add more features to the feature vector (features=[]) representing a cell trace

    #Function extract receives as input two sequences:
    #    times: timestamp of each cell
    #    sizes: direction of each cell (-1 / +1)

    #As of now, the only feature being used to distinguish between page loads is the total
    # amount of cells in each cell sequence and is given by len(times).

    # Shall some feature be missing due to impossibility of its calculation, 
    #please replace its value with "X". It will be replaced later.

def extract(times, sizes):
    features = []

    num_neg=0 #numero na direcao -1
    num_pos=0 #numero na direcao 1
    num_total= len(times) #numero total

    num_muda=0 #numero de vezes que a direcao muda
    num_igual=0 #numero de vezes que a direcao se mantem

    pos_neg=0 #numero de vezes que passa de pos para neg
    pos_pos=0 #numero de vezes que passa de pos para pos

    time_pos_neg=0
    time_pos_pos=0
    time_equal=0
    time_pos=0 #tempo total na direcao 1
    time_neg=0 #tempo total na direcao -1
    time_total= times[len(times)-1] #tempo total

    media_time_pos = 0
    max_diff = 0
    diff=0
    indice_max = 0
    count_pos_seq = 0

    soma_seq_dois=0
    soma_seq_tres=0
    soma_seq_quatro=0
    
    seq_pos_um = 0
    seq_pos_dois = 0
    seq_pos_tres = 0
    seq_pos_quatro = 0
    seq_pos_cinco = 0
    seq_pos_seis = 0
    seq_pos_sete = 0

    media_seq_dois=0    
    media_seq_tres=0
    media_seq_quatro=0
    media_indices = 0
    media_indices_metade = 0
    media_indices_quarto = 0
    media_ind_igual =0

    soma_indices = 0
    soma_indices_metade = 0
    soma_indices_quarto = 0
    soma_ind_igual = 0

    desvio = 0
    desvio_metade = 0
    desvio_igual = 0

    vet_pos = []
    vet_pos_metade = []


    for i in range(len(sizes)):
	
	if i > 0:
		diff= times[i]-times[i-1]
 
	if diff == 0:
		soma_ind_igual += i
		time_equal += 1

	if diff > max_diff:
		max_diff = diff


	if sizes[i]== -1: #analisar um -1
		num_neg = num_neg + 1;
		time_neg = time_neg + diff

		if i == 0:
			time_neg = times[i]

		else:
			if sizes[i-1] == -1: #se a anterior foi -1
				num_igual = num_igual + 1                             			
			else: #se a anterior foi +1
				num_muda = num_muda + 1
				

	else: #analisar um +1
		soma_indices += i
		vet_pos.append(i)
		if i <= (len(sizes)/2):
			soma_indices_metade += i
			vet_pos_metade.append(i)
		if i <= (len(sizes)/4):
			soma_indices_quarto += i
		num_pos = num_pos + 1;
		time_pos = time_pos + diff

		if i == 0:
			time_pos = times[i]
		else:
			if sizes[i-1] == 1: #se a anterior foi +1
				num_igual = num_igual + 1
				pos_pos = pos_pos + 1 
				time_pos_pos= time_pos_pos + diff
				count_pos_seq += 1
			else: #se a anterior foi -1
				num_muda = num_muda + 1
				pos_neg = pos_neg + 1
				time_pos_neg= time_pos_neg + diff				
				if count_pos_seq == 1:
					seq_pos_dois +=1
					soma_seq_dois += 2*i - 3
				elif count_pos_seq == 2:
					seq_pos_tres +=1
					soma_seq_tres += 3*i - 6
				elif count_pos_seq == 3:
					seq_pos_quatro +=1
					soma_seq_quatro += 4*i -10
				elif count_pos_seq == 4:
					seq_pos_cinco +=1
				elif count_pos_seq == 5:
					seq_pos_seis +=1
				elif count_pos_seq == 6:
					seq_pos_sete +=1
				count_pos_seq = 0				

    #media		
    media_indices = float(soma_indices) / float(num_pos) 
    media_indices_metade = float(soma_indices_metade) / float(num_pos / 2.0)
    media_indices_quarto = float(soma_indices_quarto) / float(num_pos / 4.0)

    #desvio
    for i in range(len(vet_pos)):
	desvio += (vet_pos[i] - media_indices)**2
    desvio = math.sqrt(float(desvio) / float(num_pos))

    for i in range(len(vet_pos_metade)):
	desvio_metade += (vet_pos_metade[i] - media_indices_metade)**2
    desvio_metade = math.sqrt(float(desvio_metade) / float(num_pos))

    #sequencias
    if num_igual != 0:
    	media_ind_igual = float(soma_ind_igual) / float(num_igual)

    if seq_pos_dois !=0:
    	media_seq_dois = float(soma_seq_dois) / float(seq_pos_dois)
	
    if seq_pos_tres !=0:
    	media_seq_tres = float(soma_seq_tres) / float(seq_pos_tres)

    if seq_pos_quatro !=0:
    	media_seq_quatro = float(soma_seq_quatro) / float(seq_pos_quatro)

    
    #percentagens
    per_num = float(num_neg) / float(num_pos)
    per_neg = float(num_neg) / float(num_total)
    per_time_neg = float(time_neg) / float(time_total)

   
    ###########################################################size

    features.append(num_pos) #numero de posicoes na direcao +1
    features.append(num_total) #numero de posicoes no vetor total
    

    features.append(time_neg) #tempo passado na direcao -1
    features.append(time_pos) #tempo passado na direcao +1
    features.append(time_total) #tempo total

    features.append(max_diff) #maxima diferenca entre duas posicoes
    
    features.append(per_neg) #num de -1 a dividir pelo numero total
    features.append(per_time_neg) #tempo de -1 a dividir pelo tempo total 
    features.append(per_num) #percentagem num(-1)/num(1)

    features.append(seq_pos_dois) #numero de vezes que sequencias de dois +1 aparecem
    features.append(seq_pos_tres) #numero de vezes que sequencias de tres +1 aparecem
    features.append(seq_pos_quatro) #numero de vezes que sequencias de quatro +1 aparecem
    features.append(seq_pos_cinco) #numero de vezes que sequencias de cinco +1 aparecem
    features.append(seq_pos_seis) #numero de vezes que sequencias de seis +1 aparecem
    features.append(seq_pos_sete) #numero de vezes que sequencias de sete +1 aparecem

    ############################################################time

    features.append(media_indices) #soma dos indices de +1 / numero de posicoes de +1
    features.append(media_indices_metade) #igual mas so em metade do vetor
    features.append(media_indices_quarto) #igual mas so num quarto do vetor
    features.append(desvio) #desvio da media_indices
    features.append(desvio_metade) #desvio da media_indices_metade

    features.append(media_ind_igual) #soma dos indices de posicao com diff==0 / num de vezes que ocorre
    features.append(desvio_igual) #desvio de media_ind_igual

    features.append(media_seq_dois) #soma dos indices de sequencias de dois +1 / num de vezes que ocorre
    features.append(media_seq_tres) #soma dos indices de sequencias de dois +1 / num de vezes que ocorre
    features.append(media_seq_quatro) #soma dos indices de sequencias de dois +1 / num de vezes que ocorre

    features.append(num_igual) #numero de vezes que passa para um numero igual (+1 +1 ou -1 -1)
    features.append(num_muda) #numero de vezes que passa para um numero diferente (+1 -1 ou -1 +1)

    features.append(pos_pos) #numero de vezes que passa de +1 para +1 
    features.append(pos_neg) #numero de vezes que passa de +1 para -1

    features.append(time_pos_pos) #somas dos tempos de celulas de +1 para +1
    features.append(time_pos_neg) #somas dos tempos de celulas de +1 para -1

    features.append(time_equal) #numero de vezes que o tempo nao altera entre duas posicoes

    return features


def impute_missing(x):
        """Accepts a list of features containing 'X' in
        place of missing values. Consistently with the code
        by Cai et al, replaces 'X' with -1.
        """
        for i in range(len(x)):
            if x[i] == 'X':
                x[i] = -1


if __name__ == '__main__':
    parser = argparse.ArgumentParser(description='Extract feature vectors')
    parser.add_argument('--traces', type=str, help='Original traces directory.',
                        required=True)
    parser.add_argument('--out', type=str, help='Output directory for features.',
                        required=True)
    args = parser.parse_args()

    if not os.path.isdir(args.out):
        os.makedirs(args.out)

    #this takes quite a while
    print "Gathering features for monitored sites..."
    for site in range(0, 100):
        print site
        for instance in range(0, 90):
            fname = str(site) + "-" + str(instance)
            #Set up times, sizes
            f = open(args.traces + "/" + fname, "r")
            times = []
            sizes = []
            for x in f:
                x = x.split("\t")
                times.append(float(x[0]))
                sizes.append(int(x[1]))
            f.close()
    
            #Extract features. All features are non-negative numbers or X. 
            features = extract(times, sizes)

            #Replace X by -1 (Cai et al.)
            impute_missing(features)

            fout = open(args.out + "/" + fname + ".features", "w")
            for x in features[:-1]:
                fout.write(repr(x) + ",")
            fout.write(repr(features[-1]))
            fout.close()

    print "Finished gathering features for monitored sites."

    print "Gathering features for non-monitored sites..."
    #open world
    for site in range(0, 9000):
        print site
        fname = str(site)
        #Set up times, sizes
        f = open(args.traces + "/" + fname, "r")
        times = []
        sizes = []
        for x in f:
            x = x.split("\t")
            times.append(float(x[0]))
            sizes.append(int(x[1]))
        f.close()
    
        #Extract features. All features are non-negative numbers or X. 
        features = extract(times, sizes)

        #Replace X by -1 (Cai et al.)
        impute_missing(features)

        fout = open(args.out + "/" + fname + ".features", "w")
        for x in features[:-1]:
            fout.write(repr(x) + ",")
        fout.write(repr(features[-1]))
        fout.close()

    print "Finished gathering features for non-monitored sites."
    f.close()
