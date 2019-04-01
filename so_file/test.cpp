//调用结构体
#include<iostream>
#include<malloc.h>
#include<string.h>
using namespace std;

typedef struct student{
    int a;
    char *path;
}STU;

//传输结构体参数
void show(STU *t){

    t->a = 99;
    cout << t->a <<endl;
    cout <<t->path << endl;
}

//返回结构体参数
STU * re_test(){
    STU *r = (STU *)malloc(sizeof(STU));
    r->a = 12;
    r->path = "return_test";
    return r;
}

//编译C++，一定要加extern "C"，注意C为大写，小写会无法识别
extern "C"
{
   void cshow(STU *t)
   {
        show(t);
   }

   STU * cre_test()
   {
        re_test();
   }
}
