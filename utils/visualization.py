
from matplotlib import pyplot as plt
import matplotlib.gridspec as gridspec
import os

def make_and_save_ts_images(images,name,samples_dir):
  class_name = "Jumping"
  
  samples = images[:10].cpu().numpy()
  if args.generator == "crnn":
      samples = np.transpose(samples, (0, 2, 1))
      samples = np.expand_dims(samples, axis=2)
  fig, axs = plt.subplots(2, 5, figsize=(20,5))
  fig.suptitle(f'Synthetic {class_name}', fontsize=30)
  for i in range(2):
      for j in range(5):
          #axs[i, j].plot(samples[i*5+j][0][0][0][:])
          #axs[i, j].plot(samples[i*5+j][0][1][0][:])
          #axs[i, j].plot(samples[i*5+j][0][2][0][:])
          axs[i, j].plot(samples[i*5+j][0][0])
          axs[i, j].plot(samples[i*5+j][1][0])
          axs[i, j].plot(samples[i*5+j][2][0])
          
  plt.savefig(
        os.path.join(samples_dir, f'{name}.png'),
        bbox_inches='tight')
  plt.close(fig)
  return True

#%% Necessary Packages

from sklearn.manifold import TSNE
from sklearn.decomposition import PCA
import matplotlib.pyplot as plt
import numpy as np

#%% PCA Analysis
    
def PCA_Analysis (dataX, dataX_hat,name,dir):

    ## TIMEGAN PAPER
  
    # Analysis Data Size
    
    if len(dataX) < 1000:
      Sample_No = len(dataX)
    else:
      Sample_No = 1000

    # Data Preprocessing
    for i in range(Sample_No):
        if (i == 0):
            arrayX = np.reshape(np.mean(np.asarray(dataX[0]),1), [1,len(dataX[0][:,0])])
            arrayX_hat = np.reshape(np.mean(np.asarray(dataX_hat[0]),1), [1,len(dataX[0][:,0])])
        else:
            arrayX = np.concatenate((arrayX, np.reshape(np.mean(np.asarray(dataX[i]),1), [1,len(dataX[0][:,0])])))
            arrayX_hat = np.concatenate((arrayX_hat, np.reshape(np.mean(np.asarray(dataX_hat[i]),1), [1,len(dataX[0][:,0])])))
    
    # Parameters        
    No = len(arrayX[:,0])
    colors = ["red" for i in range(No)] +  ["blue" for i in range(No)]    
    
    # PCA Analysis
    pca = PCA(n_components = 2)
    pca.fit(arrayX)
    pca_results = pca.transform(arrayX)
    pca_hat_results = pca.transform(arrayX_hat)
        
    # Plotting
    f, ax = plt.subplots(1)
    
    plt.scatter(pca_results[:,0], pca_results[:,1], c = colors[:No], alpha = 0.2, label = "Original")
    plt.scatter(pca_hat_results[:,0], pca_hat_results[:,1], c = colors[No:], alpha = 0.2, label = "Synthetic")

    ax.legend()
    
    plt.title('PCA plot')
    plt.xlabel('x-pca')
    plt.ylabel('y_pca')
    #plt.show()
    plt.savefig(
        os.path.join(dir, f'{name}.png'),
        bbox_inches='tight')
    plt.close()
    return True
    

def do_PCA_Analysis(args,samples_gen,name, directory):

    samples_gen = samples_gen.cpu()
    samples_gen = np.array(samples_gen)
    if args.generator != "crnn":
      samples_gen = np.squeeze(samples_gen, axis=2)
      samples_gen = np.transpose(samples_gen, (0, 2, 1))
    seq_len = args.seq_length
    features = args.features

    if args.dataset_type == "Sine":
        dataX = sine_data_generation(1000, seq_len, features)
        PCA_Analysis(dataX,samples_gen,name, directory)
    elif args.dataset_type == "Chickenpox":
        dataX = chickenpox_data_loading (seq_len)
        PCA_Analysis(dataX,samples_gen,name, directory)
    elif args.dataset_type == "Stock":
        dataX = google_data_loading (seq_len)
        PCA_Analysis(dataX[:1000],samples_gen,name, directory)
    elif args.dataset_type == "Energy":
        dataX = energy_data_loading (seq_len)
        PCA_Analysis(dataX[:1000],samples_gen,name, directory)


        
    
    
#%% TSNE Analysis
    
def tSNE_Analysis (dataX, dataX_hat,name,dir):

    ## TIMEGAN PAPER
  
    # Analysis Data Size
    if len(dataX) < 1000:
      Sample_No = len(dataX)
    else:
      Sample_No = 1000
  
    # Preprocess
    for i in range(Sample_No):
        if (i == 0):
            arrayX = np.reshape(np.mean(np.asarray(dataX[0]),1), [1,len(dataX[0][:,0])])
            arrayX_hat = np.reshape(np.mean(np.asarray(dataX_hat[0]),1), [1,len(dataX[0][:,0])])
        else:
            arrayX = np.concatenate((arrayX, np.reshape(np.mean(np.asarray(dataX[i]),1), [1,len(dataX[0][:,0])])))
            arrayX_hat = np.concatenate((arrayX_hat, np.reshape(np.mean(np.asarray(dataX_hat[i]),1), [1,len(dataX[0][:,0])])))
     
    # Do t-SNE Analysis together       
    final_arrayX = np.concatenate((arrayX, arrayX_hat), axis = 0)
    
    # Parameters
    No = len(arrayX[:,0])
    colors = ["red" for i in range(No)] +  ["blue" for i in range(No)]    
    
    # TSNE anlaysis
    tsne = TSNE(n_components = 2, verbose = 0, perplexity = 40, n_iter = 300)
    tsne_results = tsne.fit_transform(final_arrayX)
    
    # Plotting
    f, ax = plt.subplots(1)
    
    plt.scatter(tsne_results[:No,0], tsne_results[:No,1], c = colors[:No], alpha = 0.2, label = "Original")
    plt.scatter(tsne_results[No:,0], tsne_results[No:,1], c = colors[No:], alpha = 0.2, label = "Synthetic")

    ax.legend()
    
    plt.title('t-SNE plot')
    plt.xlabel('x-tsne')
    plt.ylabel('y_tsne')
    #plt.show()
    plt.savefig(
        os.path.join(dir, f'{name}.png'),
        bbox_inches='tight')
    plt.close()
    return True

def do_tSNE_Analysis(args,samples_gen,name, directory):

    samples_gen = samples_gen.cpu()
    samples_gen = np.array(samples_gen)
    if args.generator != "crnn":
      samples_gen = np.squeeze(samples_gen, axis=2)
      samples_gen = np.transpose(samples_gen, (0, 2, 1))
    seq_len = args.seq_length
    features = args.features

    if args.dataset_type == "Sine":
        dataX = sine_data_generation(1000, seq_len, features)
        tSNE_Analysis(dataX,samples_gen,name, directory)

    elif args.dataset_type == "Stock":
        dataX = google_data_loading (seq_len)
        tSNE_Analysis(dataX[:1000],samples_gen,name, directory)

    elif args.dataset_type == "Chickenpox":
        dataX = chickenpox_data_loading(seq_len)
        tSNE_Analysis(dataX,samples_gen,name, directory)

    elif args.dataset_type == "Energy":
        dataX = energy_data_loading (seq_len)
        tSNE_Analysis(dataX[:1000],samples_gen,name, directory)
