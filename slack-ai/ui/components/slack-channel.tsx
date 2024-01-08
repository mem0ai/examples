"use client";

import * as React from "react";
import axios from "axios";
import { useState, useEffect } from "react";
import { Button } from "@/components/ui/button";
import { toast } from "@/components/ui/use-toast";
import { ResetIcon } from "@radix-ui/react-icons";

import {
  Select,
  SelectContent,
  SelectItem,
  SelectTrigger,
  SelectValue,
} from "@/components/ui/select";

export function SelectSlackChannel() {
  const [channels, setChannels] = useState([]);
  const [selectedChannel, setSelectedChannel] = useState("");
  const [isLoading, setIsLoading] = useState(false);

  const addChannel = async () => {
    setIsLoading(true);
    const payload = {
      channel: selectedChannel,
    };

    try {
      await axios.post("/api/v1/add", payload);
      setIsLoading(false);
      toast({
        title: "Success",
        description: "Added data from channel " + selectedChannel,
      });
    } catch (error) {
      setIsLoading(false);
      toast({
        title: "Failed",
        description: "Failed to add data from channel " + selectedChannel,
      });
    }
  };

  const resetApp = async () => {
    try {
      await axios.get("/api/v1/reset");
      toast({
        title: "Success",
        description: "Successfully reset the app",
      });
    } catch (error) {
      toast({
        title: "Failed",
        description: "Failed to reset the app",
      });
    }
  };
  useEffect(() => {
    const getChannels = async () => {
      try {
        const response = await axios.get("/api/v1/channels");
        const channelNames = response?.data?.message?.map((m) => "# " + m.name);
        setChannels(channelNames);
      } catch (error) {
        console.log("Error getting channels from Slack. Please try again.");
      }
    };

    getChannels();
  }, []);

  return (
    <div className="mt-2 flex justify-left space-x-2">
      <Select value={selectedChannel} onValueChange={setSelectedChannel}>
        <SelectTrigger className="w-[280px]">
          <SelectValue placeholder="Select your channel" />
        </SelectTrigger>
        <SelectContent>
          {channels.map((channel) => (
            <SelectItem key={channel} value={channel}>
              {channel}
            </SelectItem>
          ))}
        </SelectContent>
      </Select>
      <Button
        className="w-[160px] bg-[#007a5a] hover:bg-[#007a5a]"
        onClick={addChannel}
        disabled={isLoading}
      >
        {isLoading ? "Adding..." : "Add channel data"}
      </Button>
      <Button className="bg-red-500 hover:bg-red-400" onClick={resetApp}>
        <ResetIcon />
      </Button>
    </div>
  );
}
