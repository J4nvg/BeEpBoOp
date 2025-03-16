import {
    Cpu,
    CircuitBoardIcon as Motherboard,
    CpuIcon as Gpu,
    MemoryStickIcon as Memory,
    HardDrive,
    Power,
    Fan,
    Square,
    LucideIcon
  } from "lucide-react"


export interface Component {
    id: number 
    name: string
    price: number
    specs?: string | "description here"
    link: string
    type: string
    recommended?: boolean
    imageUrl?: string
  }

export interface Component_final {
    SKU: number 
    name: string
    price: number
    link: string
    image_url?: string
    type: string
  }
  
export interface ComponentType {
    id: string
    label: string
    icon: LucideIcon
  }
  
export const componentTypes: ComponentType[] = [
    { id: "cpu", label: "CPU", icon: Cpu },
    { id: "mb", label: "Motherboard", icon: Motherboard },
    { id: "gpu", label: "GPU", icon: Gpu },
    { id: "ram", label: "RAM", icon: Memory },
    { id: "storage", label: "Storage", icon: HardDrive },
    { id: "cooling", label: "Cooling", icon: Fan },
    { id: "case", label: "Case", icon: Square },
    { id: "psu", label: "Power Supply", icon: Power },
    // { id: "cpus", label: "CPU", icon: Cpu },
    // { id: "mbs", label: "Motherboard", icon: Motherboard },
    // { id: "gpus", label: "GPU", icon: Gpu },
    // { id: "rams", label: "RAM", icon: Memory },
    // { id: "storages", label: "Storage", icon: HardDrive },
    // { id: "coolings", label: "Cooling", icon: Fan },
    // { id: "cases", label: "Case", icon: Square },
    // { id: "psus", label: "Power Supply", icon: Power },
  ]