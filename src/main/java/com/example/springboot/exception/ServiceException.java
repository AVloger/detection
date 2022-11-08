package com.example.springboot.exception;

import lombok.Getter;

/**
 * @author zj
 * @date 2022/4/6 14:03
 * 自定义异常
 */

@Getter
public class ServiceException extends RuntimeException {
    private String code;

    public ServiceException(String code, String msg) {
        super(msg);
        this.code = code;
    }

}