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
    id: number | string
    name: string
    price: number
    specs: string
    imageUrl?: string
    link: string
    type: string
    recommended?: boolean
  }
  
export interface ComponentType {
    id: string
    label: string
    icon: LucideIcon
  }
  
export const componentTypes: ComponentType[] = [
    { id: "cpu", label: "CPU", icon: Cpu },
    { id: "motherboard", label: "Motherboard", icon: Motherboard },
    { id: "gpu", label: "GPU", icon: Gpu },
    { id: "ram", label: "RAM", icon: Memory },
    { id: "storage", label: "Storage", icon: HardDrive },
    { id: "power", label: "Power Supply", icon: Power },
    { id: "cooling", label: "Cooling", icon: Fan },
    { id: "case", label: "Case", icon: Square },
  ]