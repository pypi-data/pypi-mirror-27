// {{f_name}}.{{ext}} create by {{user_name}} on {{date_time}}

#pragma once

#include <cocos2d.h>

using namespace cocos2d;

class {{class_name}} : public Layer{

public:
    static Scene* createScene();
    virtual bool init();
    
    CREATE_FUNC({{class_name}});
    
    
};
