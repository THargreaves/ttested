---
title: "Principal Component Regression as Pseudo-Loadings"
date: '2022-08-14'
excerpt: "Principal component regression is a powerful technique from high-dimensional statistics. In this post I offer an alternative interpretation of the procedure as a way of generating PCA loadings for new covariates."
thumbnail: /gallery/thumbnails/pseudo-loadings.jpg
toc: true
categories:
- [Statistics]
tags:
- lesson
- no-coding
---

Principal component regression (PCR) is a standard statistical technique for performing regression in high dimensions. It involves first projecting your data to a lower-dimensional space using principal component analysis (PCA) and then regressing a covariate on the projected data using standard methods (most commonly least-squares). This procedure is beneficial when the majority of the signal in the data is contained in a linear subspace of low rank, and so by only regressing on this space we avoid issues of colinearity and increased prediction error from regressing on noise.

Whilst working with PCR, I came across an interesting property of the procedure which provides a new interpretation of its output. I was unable to find any discussion of this result online (though maybe I just don't know the correct terminology to search for) so decided to briefly cover it here.

## Review of PCA and PCR

I will start by quickly recapping the key ideas behind PCA and PCR. For a more detailed account of these techniques, I strongly recommend Steve Brunton's [video](https://www.youtube.com/watch?v=fkf4IBRSeEc) on the topic, which accompanies his textbook [Data-Driven Science and Engineering](http://databookuw.com).

Given an $n \times p$ data matrix $X$—which we assume has centred columns—it is most convenient for us to view PCA as an eigen-decomposition of the sample covariance matrix 

$$\Sigma := \frac{1}{n-1}X^TX.$$

Specifically, we write

$$\Sigma = P D P^T$$

where $P$ is orthogonal and $D$ is diagonal. Further, we sort the elements of $D$ and corresponding columns of $P$ so that $d_{1, 1} \geq \ldots \geq d_{p, p}$. Note also, that $\Sigma$ is positive semi-definite by definition, so $d_{p, p} \geq 0$.

We can view $P$ as a change of basis matrix with new axes given by the columns of $P$, which we call principal directions. Each of these principal directions can be viewed as a unit vector in our original data space and we call the elements of this vector the loadings of principal direction. This can be thought of as the contribution of each original predictor to the new axis. It is important to note that these new axes are orthogonal (since $P$ is) and they are ranked by how much variation in the data they explain (due to our ordering of the $d_{i,i}$'s).

Finally, the $n \times p$ matrix $XP$ gives the coordinates of our data in this new space, which we call the principal components. In practice, we only want to retain the first $k$ dimensions of this new space, for [some choice](https://www.mikulskibartosz.name/pca-how-to-choose-the-number-of-components/) of $k$. This makes sense, since we have captured most of the variation of the data in the first principle directions, corresponding to larger values of $d_{i, i}$. We write $P^{(k)}$ for the truncation of $P$ to the $n \times k$ matrix containing its first $k$ columns.

Principal component regression is then simply the process of regressing another covariate $Y$ on the design matrix $Z = XP^{(k)}$.

## Pseudo-Loadings

So far, this is pretty textbook stuff. My insight came from setting $Y = X_k$ (the $k$th column of $X$) and $k = p$, so that $P^{(k)} = P$. In doing so, we find that the regression procedure retrieves our original principle direction as the least-squares estimator,

$$
\begin{align}
\hat{\beta} &= (Z^TZ)^{-1}Z^TY \\\\
&= (P^TX^TXP)^{-1}P^TX^TX_k \\\\
&= (P^TP\Sigma P^TP)^{-1}P^TP\Sigma P_k \\\\
&= P_k
\end{align}
$$

In other words, given our principal components alone, we can retrieve the loadings for the $k$th principal direction by regression $kth$ covariate on our principle component matrix.

This leads us to consider the behaviour of principal component regression when we set $Y=X_0$—a new covariate. We can define 

$$P_0 := \hat\beta = (P^TX^TXP)^{-1}P^TX^TX_0 = \frac{1}{(n-1)}D^{-1}P^TX^TX_0$$

to be the vector of "pseudo-loadings" for $X_0$.

Importantly, this is not the same as the true loading of $X_0$ from performing PCA on the augmented matrix 

$$
\left(\begin{array}{c|c}
  X
  &
  X_0
\end{array}\right)
.$$

Instead, we view it as the predicted loadings of $X_0$ from a PCA model trained only on $X$.

## Applications

There are two use cases that I can see this technique being of use for.

The first is as a form of robust PCA when one column has been contaminated with noise. Performing PCA on the entire dataset will corrupt the loadings for the clean covariates. Instead, PCA can be performed on only these columns, and then the above method can be used to obtain pseudo-loadings for the noisy data. From experimenting with this (though I have not attempted a formal proof), I have reason to believe that this also acts as a form of regularisation on the pseudo-loadings.

A second application applies to the case where $X_0$ contains missing values but $X$ is complete. The standard approaches to this scenario are imputation or deletion of rows with missing values. The first method is flawed because the choice of imputation method will impact the loadings obtained for the complete columns, and the second is clearly a poor choice as it wastes data. Instead, we could perform PCA on the complete columns and then compute pseudo-loadings for $X_0$ by using the subset of rows of $X$ corresponding to the non-missing values of $X_0$. Since $P$ was computed using the entirety of $X$, we take advantage of this data without letting the missingness of values in $X_0$ corrupt our loadings for the complete $X$.
