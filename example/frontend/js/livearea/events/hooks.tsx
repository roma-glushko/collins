import {useEffect, useState} from 'react';
import { uuid } from "../../utils";
import { Events } from "./entities";

const events = new Map()
const subscriberCache = new Map()

interface EventSubscriber<T extends {}> {
  <K extends keyof T>(event: K, callback: (data: T[K]) => void): () => void;
}

interface EventEmitter<T extends {}> {
  <K extends keyof T>(event: K, data: T[K]): void;
}

export const useEvent: EventSubscriber<Events> = (event, callback) => {
  const [subscriberID, _] = useState(uuid())

  useEffect(() => {
    return (): void => {
      events.get(event).delete(subscriberCache.get(subscriberID))
      subscriberCache.delete(subscriberID)
    }
  }, [])

  if (subscriberCache.has(subscriberID)) {
    events.get(event).delete(subscriberCache.get(subscriberID))
    events.get(event).add(callback)
    subscriberCache.set(subscriberID, callback)
  }

  if (!subscriberCache.has(subscriberID)) {
    if (!events.has(event)) {
      events.set(event, new Set())
    }

    events.get(event).add(callback)
    subscriberCache.set(subscriberID, callback)
  }

  return () => {
    events.get(event).delete(callback)
    subscriberCache.delete(subscriberID)
  }
}

export const useEmitter = (): EventEmitter<Events> => {
  return (event, data) => {
    const subscribers = events.get(event)

    if (subscribers == undefined) {
      return
    }

    subscribers.forEach(subscriber => {
      subscriber(data)
    })
  }
}