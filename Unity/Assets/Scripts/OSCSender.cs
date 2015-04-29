﻿using UnityEngine;
using System.Collections;

public class OSCSender : MonoBehaviour {

	public void MouseSqueak(){
		OSCHandler.Instance.SendMessageToClient("Pyo", "/mj/mouse/squeak", 1);
		OSCHandler.Instance.SendMessageToClient("Pyo", "/mj/mouse/squeak", 0);
	}



	// Use this for initialization
	void Start () {
		OSCHandler.Instance.Init(); //init OSC
	
	}
	
	// Update is called once per frame
	void Update () {
	
	}
}
