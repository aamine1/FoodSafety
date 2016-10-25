#install.packages('tm')
#install.packages('SnowballC')
#install.packages('igraph')
#install.packages('dplyr')

library(tm)
library(SnowballC)
library(igraph)
library(dplyr)

# Step 1: Convert to a corpus

product_diversity <- function(productIG, sparsity=0.95) {

corpus = Corpus(VectorSource(productIG$product))

# Step 2: Change all the text to lower case.

corpus = tm_map(corpus, tolower)

corpus = tm_map(corpus, PlainTextDocument)

# Step 3: Remove all punctuation.

corpus = tm_map(corpus, removePunctuation)

# Step 4: Remove stop words.  

corpus = tm_map(corpus, removeWords, stopwords("english"))

# Step 5: Stem document 

corpus = tm_map(corpus, stemDocument)

# Step 6: Create a word count matrix (rows are shipments, columns are words)

frequencies = DocumentTermMatrix(corpus)

# Step 7: Account for sparsity

# Use findFreqTerms to get a feeling for which words appear the most

# Words that appear at least 100 times:

findFreqTerms(frequencies, lowfreq=100)

# keep terms that appear in 5% or more of the product descriptions

sparse = removeSparseTerms(frequencies, sparsity)

# Step 8: Create data frame from the document-term matrix

allproductTM = matrix(sparse)

allproductTM[allproductTM > 1] <- 1

allproductsTM = data.frame(allproductTM)

allproductsTM = cbind(allproductTM, consignee=productIG$consignee) 

product_count <- summarize(group_by(allproductTM, consignee),sum(allproductTM[,1:length(allproductTM)-1]))

products <- t(product_count)%*%product_count

diag(products) <- 0

#Choose specific products

products <- products[c(3,16,22,23,32,61,71,74),c(3,16,22,23,32,61,71,74)]

g <- graph.adjacency(products, mode="undirected", weighted=TRUE)

fc <- fastgreedy.community(g)

fc=spinglass.community(g)

colors <- rainbow(max(membership(fc)))

#plot(g,edge.label=round(E(g)$weight, 3),vertex.color=colors[membership(fc)], layout=layout.fruchterman.reingold)

#Compute consignee's product diversity feature

consignees=unique(productIG$consignee)

productIG$product.name=rep(0,nrow(productIG))

product_names <- toupper(colnames(products))

for (i in 1:nrow(productIG)) {
  for (j in 1:length(product_names)){
    prod=product_names[j]
    if (grepl(as.character(prod),as.character(productIG$product[i]))){
      productIG$product.name[i]=as.character(prod)
      break
    }
  }
}

productIG <- subset(productIG,productIG[,4]!=0)

d=data.frame(consignees,product_diversity=rep(0,length(consignees)))

for (i in 1:length(consignees)){
  consignee_products <- unique(productIG[productIG[,1]==consignees[i],4])
  membership <- rep(-1,length(product_names))
  if (length(consignee_products)>1){
    for (j in 1:length(consignee_products)){
      for (k in 1:length(product_names)){
        if (product_names[k] == consignee_products[j]){
          membership[k]<-1
        }
      
      }
    }
    d[i,2] <- - modularity(g, membership)
  }
}

return(d)

}