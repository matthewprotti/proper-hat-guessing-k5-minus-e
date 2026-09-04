#include <algorithm>
#include <array>
#include <cassert>
#include <chrono>
#include <cstdint>
#include <fstream>
#include <iomanip>
#include <iostream>
#include <queue>
#include <random>
#include <sstream>
#include <string>
#include <vector>
using namespace std;
static constexpr int P=13, INF=13, Q=14, K=6;
int modp(long long x){x%=P;if(x<0)x+=P;return(int)x;}
int invp(int a){int e=P-2,r=1,b=modp(a);while(e){if(e&1)r=modp(1LL*r*b);b=modp(1LL*b*b);e>>=1;}return r;}
pair<int,int> proj(int x){return x==INF?make_pair(1,0):make_pair(x,1);}
int det(pair<int,int>u,pair<int,int>v){return modp(1LL*u.first*v.second-1LL*u.second*v.first);}
int mapbase(int x,int a,int b,int c){auto X=proj(x),A=proj(a),B=proj(b),C=proj(c);int num=modp(1LL*det(X,B)*det(C,A)),den=modp(1LL*det(X,A)*det(C,B));return den==0?INF:modp(1LL*num*invp(den));}
int encode_key(int j,int r0,int r1,int nx,int ny){return ((((j*Q+r0)*Q+r1)*Q+nx)*Q+ny);}
array<int,5> decode_key(int id){array<int,5>a{};for(int i=4;i>=1;i--){a[i]=id%Q;id/=Q;}a[0]=id;return a;}
struct Rec {array<int,K> edge,target; array<int,K> clique; int x,y;};
struct HK{
 int nL,nR; const vector<Rec>&rec; vector<int>L,R,dist,it;
 HK(const vector<Rec>&r,int nr):nL(r.size()),nR(nr),rec(r),L(nL,-1),R(nR,-1),dist(nL),it(nL){}
 bool bfs(){queue<int>q;bool found=false;int BIG=nL+1;for(int u=0;u<nL;u++){if(L[u]<0){dist[u]=0;q.push(u);}else dist[u]=BIG;}while(!q.empty()){int u=q.front();q.pop();for(int v:rec[u].edge){int z=R[v];if(z<0)found=true;else if(dist[z]==BIG){dist[z]=dist[u]+1;q.push(z);}}}return found;}
 bool dfs(int u){for(int&ii=it[u];ii<K;ii++){int v=rec[u].edge[ii],z=R[v];if(z<0||(dist[z]==dist[u]+1&&dfs(z))){L[u]=v;R[v]=u;return true;}}dist[u]=nL+1;return false;}
 int run(){int m=0;while(bfs()){fill(it.begin(),it.end(),0);for(int u=0;u<nL;u++)if(L[u]<0&&dfs(u))m++;}return m;}
};
int main(int argc,char**argv){
 if(argc<2){cerr<<"usage: build_k8e_strategy OUTPUT_DIR\n";return 2;}string outdir=argv[1];system(("mkdir -p '"+outdir+"'").c_str());
 const int nR=K*Q*Q*Q*Q;vector<int> domain_mask(nR,0);vector<Rec> residual;residual.reserve(48510);
 struct TwinRow{array<int,K>C;int ga,gb,ia,ib;};vector<TwinRow> twinrows;twinrows.reserve(990);
 vector<int> tail={2,3,4,5,6,7,8,9,10,11,12};long long proper=0,covered=0;
 for(int ia=0;ia<11;ia++)for(int ib=0;ib<11;ib++)if(ib!=ia)for(int ic=0;ic<11;ic++)if(ic!=ia&&ic!=ib){
  array<int,K>C={INF,0,1,tail[ia],tail[ib],tail[ic]};vector<int> av;for(int z=0;z<Q;z++)if(find(C.begin(),C.end(),z)==C.end())av.push_back(z);assert(av.size()==8);int gai=(tail[ia]+tail[ib]+tail[ic])&7; int gbi=(tail[ia]+2*tail[ib]+3*tail[ic]+1)&7; if(gbi==gai) gbi=(gbi+1)&7; int ga=av[gai],gb=av[gbi];twinrows.push_back({C,ga,gb,gai,gbi});
  for(int x:av)for(int y:av){proper++;Rec r{};r.clique=C;r.x=x;r.y=y;for(int j=0;j<K;j++){array<int,5>oth{};int p=0;for(int i=0;i<K;i++)if(i!=j)oth[p++]=i;int a=C[oth[0]],b=C[oth[1]],c=C[oth[2]],r0=mapbase(C[oth[3]],a,b,c),r1=mapbase(C[oth[4]],a,b,c),nx=mapbase(x,a,b,c),ny=mapbase(y,a,b,c),t=mapbase(C[j],a,b,c);int key=encode_key(j,r0,r1,nx,ny);r.edge[j]=key;r.target[j]=t;domain_mask[key]|=1<<t;}
   if(ga==x||gb==y){covered++;continue;}residual.push_back(r);
  }
 }
 assert(twinrows.size()==990&&proper==63360&&residual.size()==48510);
 HK hk(residual,nR);int match=hk.run();if(match!=(int)residual.size()){cerr<<"deficiency "<<residual.size()-match<<"\n";return 3;}
 vector<int> clique_guess(nR,-1);for(int u=0;u<(int)residual.size();u++){int rv=hk.L[u],j=-1;for(int z=0;z<K;z++)if(residual[u].edge[z]==rv){j=z;break;}assert(j>=0);int t=residual[u].target[j];if(clique_guess[rv]>=0&&clique_guess[rv]!=t)abort();clique_guess[rv]=t;}
 int right_count=0,matched_right=0;for(int id=0;id<nR;id++)if(domain_mask[id]){right_count++;if(clique_guess[id]>=0)matched_right++;else clique_guess[id]=__builtin_ctz((unsigned)domain_mask[id]);assert(domain_mask[id]&(1<<clique_guess[id]));}
 assert(right_count==53460&&matched_right==48510);
 // direct normalized verification
 long long failures=0,hit_hist[9]={};int tri=0;
 for(auto const&tw:twinrows){auto C=tw.C;vector<int>av;for(int z=0;z<Q;z++)if(find(C.begin(),C.end(),z)==C.end())av.push_back(z);for(int x:av)for(int y:av){int hits=(tw.ga==x)+(tw.gb==y);for(int j=0;j<K;j++){array<int,5>oth{};int p=0;for(int i=0;i<K;i++)if(i!=j)oth[p++]=i;int a=C[oth[0]],b=C[oth[1]],c=C[oth[2]],r0=mapbase(C[oth[3]],a,b,c),r1=mapbase(C[oth[4]],a,b,c),nx=mapbase(x,a,b,c),ny=mapbase(y,a,b,c),t=mapbase(C[j],a,b,c);int key=encode_key(j,r0,r1,nx,ny);hits+=clique_guess[key]==t;}if(hits==0)failures++;if(hits<9)hit_hist[hits]++;tri++;}}
 assert(tri==63360&&failures==0);
 ofstream ft(outdir+"/K8_e_q14_twin_rules.tsv");ft<<"a\tb\tc\talpha\tbeta\talpha_index\tbeta_index\n";for(auto const&r:twinrows)ft<<r.C[3]<<'\t'<<r.C[4]<<'\t'<<r.C[5]<<'\t'<<r.ga<<'\t'<<r.gb<<'\t'<<r.ia<<'\t'<<r.ib<<'\n';
 ofstream fc(outdir+"/K8_e_q14_clique_rules.tsv");fc<<"right_key\tvertex\trem0\trem1\ttwin0\ttwin1\tguess\tdomain_mask\tmatched\n";for(int id=0;id<nR;id++)if(domain_mask[id]){auto a=decode_key(id);fc<<id;for(int x:a)fc<<'\t'<<x;fc<<'\t'<<clique_guess[id]<<'\t'<<domain_mask[id]<<'\t'<<(hk.R[id]>=0?1:0)<<'\n';}
 ofstream fm(outdir+"/K8_e_q14_residual_orbit_matching.tsv");fm<<"left\tright_key\tvertex\ttarget\ttwin0_colour\ttwin1_colour\tclique\n";for(int u=0;u<(int)residual.size();u++){int rv=hk.L[u],j=-1;for(int z=0;z<K;z++)if(residual[u].edge[z]==rv){j=z;break;}fm<<u<<'\t'<<rv<<'\t'<<j<<'\t'<<residual[u].target[j]<<'\t'<<residual[u].x<<'\t'<<residual[u].y<<'\t';for(int z=0;z<K;z++){if(z)fm<<',';fm<<residual[u].clique[z];}fm<<'\n';}
 ofstream fs(outdir+"/summary.json");fs<<"{\n  \"format\": \"K8-e-q14-PGL-equivariant-strategy-v1\",\n  \"claim_candidate\": \"HG_P(K8-e)=14\",\n  \"generator\": \"alpha_index=(a+b+c) mod 8; beta_index=(a+2b+3c+1) mod 8, incremented mod 8 when equal\",\n  \"normalized_clique_orbits\": 990,\n  \"normalized_proper_colouring_orbits\": "<<proper<<",\n  \"twin_covered_orbits\": "<<covered<<",\n  \"residual_orbits\": "<<residual.size()<<",\n  \"attainable_clique_view_orbits\": "<<right_count<<",\n  \"matching_size\": "<<match<<",\n  \"matched_clique_view_orbits\": "<<matched_right<<",\n  \"coverage_failures\": "<<failures<<",\n  \"correct_guess_histogram\": {";bool first=true;for(int i=0;i<9;i++)if(hit_hist[i]){if(!first)fs<<',';fs<<"\n    \""<<i<<"\": "<<hit_hist[i];first=false;}fs<<"\n  },\n  \"full_PGL_group_order\": 2184,\n  \"full_proper_colourings_represented\": "<<proper*2184LL<<",\n  \"verified\": true\n}\n";
 cout<<"FOUND K8-e q=14 PGL-equivariant strategy\n"<<"normalized="<<proper<<" residual="<<residual.size()<<" matching="<<match<<" right="<<right_count<<" failures="<<failures<<" full="<<proper*2184LL<<"\n";return 0;
}
