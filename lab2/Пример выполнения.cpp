//---------------------------------------------------------------------------
// Чуприн Сергей ИУ7-91 2009 год
//---------------------------------------------------------------------------
#include <vcl.h>
#include <list>
#include <vector>
#include <stdio.h>
#include <conio.h>

using namespace std;

#define EMPTY_SYM       '$'     // эпсилон-символ
//------------------------------------------------------------------------------
// Замена подстроки в AnsiString строке
AnsiString ReplaceStr (AnsiString srcStr, const AnsiString& replaceFrom, const AnsiString& replaceTo )
{
        int p;

        while ( (p = srcStr.Pos(replaceFrom)) != 0 )
        {
                srcStr.Delete(p,replaceFrom.Length());
                srcStr.Insert(replaceTo,p);
        } /* if */
        return srcStr;
}

AnsiString Replace1Str (AnsiString srcStr, const AnsiString& replaceFrom, const AnsiString& replaceTo )
{
        int p;

        if ( (p = srcStr.Pos(replaceFrom)) != 0 )
        {
                srcStr.Delete(p,replaceFrom.Length());
                srcStr.Insert(replaceTo,p);
        } /* if */
        return srcStr;
}
//------------------------------------------------------------------------------
struct Grammar  // Грамматика
{
        vector<char>    N,   // Нетерминалы
                        T;   // Терминалы
        vector<AnsiString> P;   // Правила
                   char S;   // Аксиома
};

int isIN ( const vector<char>& arr, char ch )
{
        for ( int p = 0; p < (int)arr.size(); ++p )
        {
                if ( arr[p] == ch ) return p;
        } /* for */
        return -1;
}

void get_new_N ( vector<char> in, vector<char>& out, int k )
{
        while ( k-- )
        {
                for ( char p = 'A'; p <= 'Z'; ++p )
                {
                        if ( isIN(in,p) == -1 )
                        {
                                in.push_back(p);
                                out.push_back(p);
                                break;
                        } /* if */
                } /* for */
        } /* while */
}

// Чтение грамматикаи
bool read_grammar ( const char* file, Grammar& g )
{
        FILE *f = fopen(file,"rb");
        if (!f) return false;
        char str[256],sym;
	int n;
                                 
        fscanf (f,"%d\n",&n);
        for ( int i = 0; i < n; ++i )
        {
                fscanf (f,"%c\n",&sym);
                g.N.push_back(sym);
        } /* for */

        fscanf (f,"%d\n",&n);
        for ( int i = 0; i < n; ++i )
        {
                fscanf (f,"%c\n",&sym);
                g.T.push_back(sym);
        } /* for */

        fscanf (f,"%d\n",&n);
        for ( int i = 0; i < n; ++i )
        {
                fscanf (f,"%s\n",&str);
                g.P.push_back(str);
        } /* for */

        fscanf (f,"%c\n",&sym);

        g.S = sym;
        fclose(f);
        return true;
}

// Печать грамматикаи
void print_grammar ( const Grammar& g, char* ss )
{
        printf("%s = {%c},{",ss,g.S);
        for ( size_t i = 0; i < g.N.size(); ++i )
        {
                if ( i == g.N.size()-1 )
                        printf("%c},{",g.N[i]);
                else
                        printf("%c,",g.N[i]);
        }

        for ( size_t i = 0; i < g.T.size(); ++i )
        {
                if ( i == g.T.size()-1 )
                        printf("%c}\n",g.T[i]);
                else
                        printf("%c,",g.T[i]);
        }

        for ( size_t i = 0; i < g.P.size(); ++i )
        printf("\t\t\t\t%s\n",g.P[i].c_str());
        printf("\n");
}

bool isEmptyP ( AnsiString str )
{
        for ( int p = 4; p <= str.Length(); ++p )
        {
                if ( str[p] != '$' ) return false;
        } /* for */
        return true;
}

// Исчезающие нетерминалы
vector<char> HideN ( const Grammar& g )
{
        vector<char> isHide,HideSym;
	char sym;
	AnsiString str;
        int count;

        for ( size_t i = 0; i < g.P.size(); ++i )
        {
                if ( g.P[i].Pos("->$") == 2 )
                {
                        isHide.push_back(g.P[i][1]);
                } /* if */
        } /* for */

        do {
                count = 0;
                for ( size_t i = 0; i < g.P.size(); ++i )
                {
                        str = g.P[i];
                        sym = g.P[i][1];
                        for ( size_t k = 0; k < HideSym.size(); ++k )
                        {
                                str = ReplaceStr ( str,HideSym[k],"$" );
                        } /* for */

                        if ( isEmptyP(str) && isIN(HideSym,sym) == -1 )
                        {
                                ++count;
                                HideSym.push_back(sym);
                        } /* if */
                } /* for */
        } while ( count != 0 );

        return HideSym;
}

//------------------------------------------------------------------------------
// Преобразование грамматики G0 в G1 к (*) по Алгоритму 8.1
//------------------------------------------------------------------------------
Grammar G_81 ( const Grammar& g0 )
{
	AnsiString str,f_str;
	Grammar res;
	vector<AnsiString> newRule;
	vector<char> HideSym, _HideSym, pp;
	int p;
	bool flag;

        // Удовлетворяет ли грамматика условию (*)?
        for ( size_t k = 0; k < g0.P.size(); ++k )
        {
                if ( g0.P[k].Length() == 4 && g0.P[k][4] == '$' )
                {
                        pp.push_back(g0.P[k][1]);
                } /* if */
        } /* for */

        flag = false;
        for ( size_t k = 0; k < g0.P.size(); ++k )
        {
                if ( g0.P[k].SubString(2,3) != "->$" && g0.P[k].Length() != 4 && (p = isIN(pp,g0.P[k][4])) != -1 )
                {
                        flag = true;
                } /* if */
        } /* for */

        if ( !flag )
        {
                res = g0;
                return res;
        } /* if */

        // Пункт 0 (копируем терминалы)
        for ( size_t k = 0; k < g0.T.size(); ++k )
        {
                res.T.push_back(g0.T[k]);
        } /* for */

        // Пункт 1 (исчезающие нетерминалы)
        HideSym = HideN(g0);
        get_new_N ( HideSym, _HideSym, HideSym.size() );

        // Пункт 2 (порождаются ли пустые цепочки грамматикой G?)
        if ( (p = isIN(HideSym,g0.S)) != -1 )
        {
                res.S = _HideSym[p];

                // Сначала добавляем аксиому
                for ( size_t k = 0; k < _HideSym.size(); ++k )
                {
                        if ( _HideSym[k] == res.S )
                        {
                                res.N.push_back(res.S);
                                break;
                        } /* if */
                } /* for */

                for ( size_t k = 0; k < g0.N.size(); ++k )
                {
                        if ( g0.N[k] != g0.S )
                        {
                                res.N.push_back(g0.N[k]);
                        } /* if */
                } /* for */

                for ( size_t k = 0; k < _HideSym.size(); ++k )
                {
                        if ( _HideSym[k] != res.S )
                        {
                                res.N.push_back(_HideSym[k]);
                        } /* if */
                } /* for */
        }
        else
        {
                // Оставляем прежнюю аксиому
                res.S = g0.S;

                for ( size_t k = 0; k < g0.N.size(); ++k )
                {
                        res.N.push_back(g0.N[k]);
                } /* for */

                for ( size_t k = 0; k < _HideSym.size(); ++k )
                {
                        res.N.push_back(_HideSym[k]);
                } /* for */
        } /* if-else */

        // Пункт 3
        for ( size_t k = 0; k < g0.P.size(); ++k )
        {
                  str = g0.P[k];
                f_str = str.SubString(1,3);

                // Пункт 4 (переносим правила вида X->$)
                if ( str[4] == '$' )
                {
                        res.P.push_back(str);
                        continue;
                } /* if */

                // Вид правила A->B1...BmX1...Xn
                for ( size_t k = 4; k <= (size_t)str.Length(); ++k )
                {
                        if ( isIN ( HideSym, str[k] ) != -1 || str[k] == '$' )
                        {
                                f_str += '0';
                        }
                        else
                        {
                                f_str += '1';
                        } /* if-else */
                } /* for */

                newRule.clear();
                // Случай а)
                if ( f_str[4] == '0' )
                {
                        p = isIN(HideSym,str[4]);
                        str = Replace1Str(str,str[4],_HideSym[p]);
                        newRule.push_back(str);
                        for ( size_t k = 4; k <= (size_t)str.Length(); ++k )
                        {
                                if ( f_str[k] == '0' )
                                {
                                        str[4] = ' ';
                                        str = Replace1Str(str," ","");
                                        p = isIN(HideSym,str[k]);
                                        str = Replace1Str(str,str[k],_HideSym[p]);
                                        newRule.push_back(str);
                                } /* if */
                        } /* for */
                } /* if */

                // Случай б)
                else if ( f_str[4] == '1' )
                {
                        newRule.push_back(str);
                } /* if-else */

                // Если символ исчезающий
                if ( (p = isIN(HideSym,newRule[0][1])) != -1 )
                {
                        for ( size_t k = 0; k < newRule.size(); ++k )
                        {
                                str = newRule[k];
                                // Если аксиома исходной гр. не совпадает с преобразованной гр.
                                if ( res.S != g0.S && str[1] != g0.S )
                                {
                                        res.P.push_back(str);
                                } /* if */

                                str[1] = _HideSym[p];
                                res.P.push_back(str);
                        } /* for */
                }
                else // Если символ неисчезающий
                {
                        for ( size_t k = 0; k < newRule.size(); ++k )
                        {
                                res.P.push_back(newRule[k]);
                        } /* for */
                } /* if-else */
        } /* for */

        return res;
}

//------------------------------------------------------------------------------
// Преобразование грамматики G1 в G2 (удаление е-правил) по Алгоритму 8.2
//------------------------------------------------------------------------------
void MakeP ( const vector<char>& HideSym, vector<AnsiString>& P, AnsiString addP )
{
        AnsiString str;
	bool flag;

        for ( int i = 4; i <= addP.Length(); ++i )
        {
                // Если найден исчезающий нетерминал
                if ( isIN ( HideSym, addP[i] ) != -1 )
                {
                        str = addP;
                        str[i] = '$';
                        str = Replace1Str(str,"$","");
                        MakeP(HideSym,P,str);
                }
        } /* for */

        if ( !(addP.Length() == 3 || addP[4] == '$' || (addP[1] == addP[4] && addP.Length() == 4)) )
        {
                bool flag = false;
                for ( size_t i = 0; i < P.size(); ++i )
                {
                        if ( P[i] == addP )
                        {
                                flag = true;
                                break;
                        } /* if */
                } /* for */

                if ( !flag ) P.push_back(addP);
        } /* if */
}

Grammar G_82 ( const Grammar& g1 )
{
	AnsiString str,f_str;
	Grammar res;
	vector<AnsiString> newRule;
	vector<char> HideSym, _HideSym, pp;
	int p;
	bool flag;

        // Копируем терминалы
        for ( size_t k = 0; k < g1.T.size(); ++k )
        {
                res.T.push_back(g1.T[k]);
        } /* for */

        // Копируем нетерминалы
        for ( size_t k = 0; k < g1.N.size(); ++k )
        {
                res.N.push_back(g1.N[k]);
        } /* for */

        // Копируем аксиому
        res.S = g1.S;

        // Исчезающие нетерминалы (A->$)
        vector<char> Ne = HideN(g1);
        vector<AnsiString> P;

        for ( size_t k = 0; k < g1.P.size(); ++k )
        {
                MakeP (Ne,P, g1.P[k]);
        } /* for */

        for ( size_t k = 0; k < P.size(); ++k )
        {
                res.P.push_back(P[k]);
        } /* for */
        
        return res;
}
//------------------------------------------------------------------------------
int main ( int argc, char* argv[] )
{
	char str[128];
	AnsiString g_path;
	Grammar g0,g1,g2;

        do {
                printf("Input file grammar: ");
                scanf("%s",str);

                g_path = AnsiString(str);
                g_path = g_path.Trim();
        } while ( g_path.IsEmpty() );

        if ( read_grammar ( g_path.c_str(), g0 ) )
        {
                print_grammar(g0,"G0");

                g1 = G_81(g0);
                print_grammar (g1,"G1");

                g2 = G_82(g0);
                print_grammar (g2,"G2");
        }
        else
        {
                printf("Can't open file!\n");
        } /* if-else */

        getch();
        return 0;
}
//------------------------------------------------------------------------------
