#include <algorithm>
#include <array>
#include <cassert>
#include <chrono>
#include <cstdint>
#include <fstream>
#include <iostream>
#include <sstream>
#include <string>
#include <vector>
using namespace std;
static constexpr int P=13,INF=13,Q=14,K=6;
int modp(long long x){x%=P;if(x<0)x+=P;return(int)x;}int invp(int a){int e=11,r=1,b=modp(a);while(e){if(e&1)r=modp(1LL*r*b);b=modp(1LL*b*b);e>>=1;}return r;}
pair<int,int> proj(int x){return x==INF?make_pair(1,0):make_pair(x,1);}int det(pair<int,int>u,pair<int,int>v){return modp(1LL*u.first*v.second-1LL*u.second*v.first);}int mapbase(int x,int a,int b,int c){auto X=proj(x),A=proj(a),B=proj(b),C=proj(c);int num=modp(1LL*det(X,B)*det(C,A)),den=modp(1LL*det(X,A)*det(C,B));return den==0?INF:modp(1LL*num*invp(den));}
int tid(int a,int b,int c){return (a*Q+b)*Q+c;}int rid(int j,int r0,int r1,int x,int y){return ((((j*Q+r0)*Q+r1)*Q+x)*Q+y);}
vector<string> split(const string&s,char d){vector<string>v;stringstream ss(s);string x;while(getline(ss,x,d))v.push_back(x);return v;}
int main(int argc,char**argv){if(argc<2){cerr<<"usage: verify_k8e_full ROOT\n";return 2;}string root=argv[1];vector<array<int,2>> twin(Q*Q*Q,{-1,-1});vector<int>clique(K*Q*Q*Q*Q,-1);
 {ifstream f(root+"/K8_e_q14_twin_rules.tsv");string s;getline(f,s);int n=0;while(getline(f,s)){auto v=split(s,'\t');if(v.size()!=7)abort();int a=stoi(v[0]),b=stoi(v[1]),c=stoi(v[2]);auto&id=twin[tid(a,b,c)];if(id[0]>=0)abort();id={stoi(v[3]),stoi(v[4])};n++;}assert(n==990);}
 {ifstream f(root+"/K8_e_q14_clique_rules.tsv");string s;getline(f,s);int n=0;while(getline(f,s)){auto v=split(s,'\t');if(v.size()!=9)abort();int id=stoi(v[0]);if(clique[id]>=0)abort();clique[id]=stoi(v[6]);n++;}assert(n==53460);}
 array<array<int,Q>,Q*Q*Q> H{};for(auto&x:H)x.fill(-1);for(int a=0;a<Q;a++)for(int b=0;b<Q;b++)if(b!=a)for(int c=0;c<Q;c++)if(c!=a&&c!=b)for(int x=0;x<Q;x++)H[tid(a,b,c)][x]=mapbase(x,a,b,c);
long long proper=0,fail=0,hist[9]={};array<int,K>C{};bool used[Q]={};
 auto rec=[&](auto&&self,int pos)->void{
  if(pos<K){for(int z=0;z<Q;z++)if(!used[z]){used[z]=true;C[pos]=z;self(self,pos+1);used[z]=false;}return;}
  auto& ht=H[tid(C[0],C[1],C[2])];auto tr=twin[tid(ht[C[3]],ht[C[4]],ht[C[5]])];assert(tr[0]>=0);vector<int>av;for(int z=0;z<Q;z++)if(!used[z])av.push_back(z);assert(av.size()==8);
  array<array<int,Q>*,K> hj{};array<int,K>r0{},r1{},target{};
  for(int j=0;j<K;j++){array<int,5>o{};int p=0;for(int i=0;i<K;i++)if(i!=j)o[p++]=i;hj[j]=&H[tid(C[o[0]],C[o[1]],C[o[2]])];r0[j]=(*hj[j])[C[o[3]]];r1[j]=(*hj[j])[C[o[4]]];target[j]=(*hj[j])[C[j]];}
  for(int x:av)for(int y:av){int hits=(tr[0]==ht[x])+(tr[1]==ht[y]);for(int j=0;j<K;j++){auto&h=*hj[j];int id=rid(j,r0[j],r1[j],h[x],h[y]);int g=clique[id];assert(g>=0);hits+=g==target[j];}proper++;if(hits==0)fail++;if(hits<9)hist[hits]++;}
 };
 rec(rec,0);cout<<"{\n  \"format\": \"K8-e-q14-full-colouring-independent-C++-verification-v1\",\n  \"proper_colourings_checked\": "<<proper<<",\n  \"coverage_failures\": "<<fail<<",\n  \"correct_guess_histogram\": {";bool first=true;for(int i=0;i<9;i++)if(hist[i]){if(!first)cout<<',';cout<<"\n    \""<<i<<"\": "<<hist[i];first=false;}cout<<"\n  },\n  \"verified\": "<<(fail==0?"true":"false")<<"\n}\n";return fail?1:0;}
