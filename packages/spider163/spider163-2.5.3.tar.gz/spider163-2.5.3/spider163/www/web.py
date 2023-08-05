#!/usr/bin/env python
# -*- coding: utf-8 -*-
from flask import Flask, request, json, jsonify
from flask import render_template, make_response

from spider163.spider import playlist
from spider163.utils import pysql

app = Flask(__name__, static_path='/static')


@app.route("/")
def index():
    return render_template('index.html')


@app.route("/spider")
def spider(type=None):
    return render_template('spider.html')


@app.route("/spider/getPlaylist", methods=['POST'])
def get_playlist():
    pl = playlist.Playlist()
    return jsonify({"test": request.form["gdType"]})


@app.route("/stat")
def statistics():
    return render_template('stat.html')


@app.route("/stat/playlist")
def stat_playlist():
    return jsonify(pysql.stat_playlist())


@app.route("/stat/music")
def stat_music():
    return jsonify(pysql.stat_music())


@app.route("/stat/dataCount")
def stat_data():
    return jsonify(pysql.stat_data())


@app.route("/scan")
def scan():
    return render_template('scan.html')


@app.route("/scan/data")
def scan_data():
    return jsonify(pysql.random_data())


@app.route("/business")
def business():
    return make_response(open('templates/business.html').read())


